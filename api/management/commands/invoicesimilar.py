import pandas as pd
from rapidfuzz import fuzz



df = pd.read_csv('Invoicesduplicates.csv')

def exact_match(row_a, row_b):
    """Coinciden exactamente los cuatro campos."""
    return (
        row_a['Invoice Reference'] == row_b['Invoice Reference'] and
        row_a['Document Date']    == row_b['Document Date']    and
        row_a['Invoice Value']    == row_b['Invoice Value']    and
        row_a['Vendor Name']      == row_b['Vendor Name']
    )

def similar_vendor(row_a, row_b, threshold=90):
    """
    - 3 campos exactos: (Invoice Reference, Document Date, Invoice Value)
    - Vendor Name fuzzy con un mínimo de similitud (threshold).
    - Se ilustran algunas limpiezas mínimas (quitar caracteres no alfanuméricos).
    """
    if (
        row_a['Invoice Reference'] == row_b['Invoice Reference'] and
        row_a['Document Date']    == row_b['Document Date']    and
        row_a['Invoice Value']    == row_b['Invoice Value']
    ):
        def clean_vendor(name):
            # Quita todo lo que no sea alfanumérico
            cleaned = ''.join(ch for ch in name if ch.isalnum())
            return cleaned.upper()

        vend_a = clean_vendor(row_a['Vendor Name'])
        vend_b = clean_vendor(row_b['Vendor Name'])
        ratio = fuzz.token_sort_ratio(vend_a, vend_b)
        return ratio >= threshold
    return False

def similar_reference(row_a, row_b, threshold=85):
    """
    - 3 campos exactos: (Document Date, Invoice Value, Vendor Name)
    - Invoice Reference fuzzy.
    - Se usa una métrica simple de similitud (rapidfuzz).
    """
    if (
        row_a['Document Date'] == row_b['Document Date'] and
        row_a['Invoice Value'] == row_b['Invoice Value'] and
        row_a['Vendor Name']   == row_b['Vendor Name']
    ):
        ref_a = ''.join(ch for ch in row_a['Invoice Reference'] if ch.isalnum())
        ref_b = ''.join(ch for ch in row_b['Invoice Reference'] if ch.isalnum())
        ratio = fuzz.token_sort_ratio(ref_a, ref_b)
        return ratio >= threshold
    return False

def similar_date(row_a, row_b, max_days=7):
    """
    - 3 columnas exactas: (Invoice Reference, Invoice Value, Vendor Name)
    - Document Date difiere a lo sumo X días (por defecto, 7 días).
    - Se podría extender para día/mes invertido, etc.
    """
    if (
        row_a['Invoice Reference'] == row_b['Invoice Reference'] and
        row_a['Invoice Value']    == row_b['Invoice Value'] and
        row_a['Vendor Name']      == row_b['Vendor Name']
    ):
        try:
            d_a = pd.to_datetime(row_a['Document Date'])
            d_b = pd.to_datetime(row_b['Document Date'])
        except:
            return False
        
        diff = abs((d_a - d_b).days)
        return diff <= max_days
    return False

def similar_value(row_a, row_b, tolerance=100):
    """
    - 3 columnas exactas: (Invoice Reference, Document Date, Vendor Name)
    - Invoice Value 'cerca' en el valor (<= tolerance).
    - O se pueden agregar más reglas (transposición de dígitos, etc.).
    """
    if (
        row_a['Invoice Reference'] == row_b['Invoice Reference'] and
        row_a['Document Date']    == row_b['Document Date'] and
        row_a['Vendor Name']      == row_b['Vendor Name']
    ):
        try:
            v_a = float(row_a['Invoice Value'])
            v_b = float(row_b['Invoice Value'])
            if abs(v_a - v_b) <= tolerance:
                return True
        except:
            pass
    return False

def get_match_patterns(row_a, row_b):
    """
    Devuelve una lista con TODOS los patrones que se cumplan
    (podría devolver más de uno a la vez si, p.ej., exact match y similar date
     se cumplen simultáneamente).
    """
    patterns = []
    if exact_match(row_a, row_b):
        patterns.append("exact match")
    if similar_vendor(row_a, row_b):
        patterns.append("similar vendor")
    if similar_reference(row_a, row_b):
        patterns.append("similar reference")
    if similar_date(row_a, row_b):
        patterns.append("similar date")
    if similar_value(row_a, row_b):
        patterns.append("similar value")
    return patterns



df["DuplicatePattern"] = ""

records = df.to_dict('records')

for i in range(len(records)):
    row_a = records[i]
   
    patterns_found = set()
    
    for j in range(len(records)):
        if i == j:
            continue
        
        row_b = records[j]
        # Obtenemos todos los patrones que se cumplan
        patterns = get_match_patterns(row_a, row_b)
        for p in patterns:
            patterns_found.add(p)
    
    # Si no encontró ningún patrón, asigna "unique"
    if len(patterns_found) == 0:
        df.loc[i, "DuplicatePattern"] = "unique"
    else:
        # Unimos todos los patrones encontrados en un solo string
        # Ordenamos alfabéticamente solo para consistencia.
        df.loc[i, "DuplicatePattern"] = ", ".join(sorted(patterns_found))


df.to_excel("datos_invoices_con_patrones.xlsx", index=False)

print("Archivo 'datos_invoices_con_patrones.csv' generado con columna 'DuplicatePattern'.")
