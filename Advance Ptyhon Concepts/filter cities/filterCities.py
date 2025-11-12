def filter_cities_ending_with_n(cities):
    """
    Filters and returns the list of city names ending with 'n' or 'N'.
    
    Parameters:
        cities (list): List of city names (strings)
    
    Returns:
        list: List of city names that end with 'n' or 'N'
    """
    result = []
    for city in cities:
        if city and city[-1].lower() == 'n':
            result.append(city)
    return result