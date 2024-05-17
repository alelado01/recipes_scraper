def clean_ingredients(ingredients):
    cleaned_ingredients = []
    for ingredient in ingredients:
        # Rimuovi '\n' e '\t' con uno spazio vuoto
        cleaned_ingredient = re.sub(r'\n|\t', '', ingredient)
        # Trova la quantità tra parentesi
        quantity_match = re.search(r'\d+(\.\d+)?\s*(g|kg|mg|ml|cl|l|oz|lb|tsp|tbsp|cup|q\.b\.|cucchiaio|cucchiaino|a piacere|a temperatura ambiente|a fette|qualche foglia|Acqua| (calda)| (naturale)| circa| pizzico| da rendere in scaglie)?[;,]?', cleaned_ingredient)
        if quantity_match:
            # Aggiungi la quantità tra parentesi subito dopo l'ingrediente
            cleaned_ingredient = re.sub(quantity_match.group(), f' ({quantity_match.group()})', cleaned_ingredient)
        cleaned_ingredients.append(cleaned_ingredient)
    return cleaned_ingredients
