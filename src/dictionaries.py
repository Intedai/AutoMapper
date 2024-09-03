def generate_dictionary(
    Albania, Austria, Belarus, Belgium, Bosnia_and_Herzegovina, Bulgaria, Croatia, 
    Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Iceland, 
    Ireland, Italy, Kosovo, Latvia, Lithuania, Luxembourg, Moldova, Montenegro, 
    Netherlands, North_Macedonia, Norway, Poland, Portugal, Romania, Russia, Serbia, 
    Slovakia, Slovenia, Spain, Sweden, Switzerland, Turkey, Ukraine, United_Kingdom
) -> dict:
    """
    Generate dictionary with country file images and their values
    :returns: the dictionary
    """
    return {
        'Albania.png': Albania, 'Austria.png': Austria, 'Belarus.png': Belarus, 
        'Belgium.png': Belgium, 'Bosnia and Herzegovina.png': Bosnia_and_Herzegovina, 
        'Bulgaria.png': Bulgaria, 'Croatia.png': Croatia, 'Czechia.png': Czechia, 
        'Denmark.png': Denmark, 'Estonia.png': Estonia, 'Finland.png': Finland, 
        'France.png': France, 'Germany.png': Germany, 'Greece.png': Greece, 
        'Hungary.png': Hungary, 'Iceland.png': Iceland, 'Ireland.png': Ireland, 
        'Italy.png': Italy, 'Kosovo.png': Kosovo, 'Latvia.png': Latvia, 
        'Lithuania.png': Lithuania, 'Luxembourg.png': Luxembourg, 'Moldova.png': Moldova, 
        'Montenegro.png': Montenegro, 'Netherlands.png': Netherlands, 
        'North Macedonia.png': North_Macedonia, 'Norway.png': Norway, 'Poland.png': Poland, 
        'Portugal.png': Portugal, 'Romania.png': Romania, 'Russia.png': Russia, 
        'Serbia.png': Serbia, 'Slovakia.png': Slovakia, 'Slovenia.png': Slovenia, 
        'Spain.png': Spain, 'Sweden.png': Sweden, 'Switzerland.png': Switzerland, 
        'Turkey.png': Turkey, 'Ukraine.png': Ukraine, 'United Kingdom.png': United_Kingdom
    }

# Position and size ratio calculated by hand to fit the best for each country when entering years
position_dict = generate_dictionary(
    Albania=(730, 1460, 0.5), 
    Austria=(572, 1260, 0.85), 
    Belarus=(810, 1020, 1), 
    Belgium=(364, 1154, 0.7), 
    Bosnia_and_Herzegovina=(656, 1360, 0.75), 
    Bulgaria=(817, 1380, 1), 
    Croatia=(615, 1322, 0.65), 
    Czechia=(580, 1184, 0.8), 
    Denmark=(469, 987, 0.75), 
    Estonia=(732, 866, 0.8), 
    Finland=(700, 750, 1), 
    France=(300, 1280, 1), 
    Germany=(468, 1143, 1), 
    Greece=(769, 1509, 1), 
    Hungary=(660, 1263, 1), 
    Iceland=(86, 610, 1), 
    Ireland=(122, 1040, 0.8), 
    Italy=(462, 1333, 1), 
    Kosovo=(743, 1404, 0.5), 
    Latvia=(726, 930, 0.8), 
    Lithuania=(732, 980, 0.8), 
    Luxembourg=(405, 1195, 0.45), 
    Moldova=(887, 1220, 0.65), 
    Montenegro=(704, 1406, 0.5), 
    Netherlands=(382, 1107, 0.7), 
    North_Macedonia=(767, 1431, 0.5), 
    Norway=(445, 825, 1), 
    Poland=(650, 1090, 1), 
    Portugal=(12, 1475, 0.7), 
    Romania=(800, 1275, 1), 
    Russia=(870, 740, 2.5), 
    Serbia=(725, 1355, 0.9), 
    Slovakia=(671, 1210, 0.70), 
    Slovenia=(585, 1309, 0.5), 
    Spain=(130, 1464, 1), 
    Sweden=(537, 752, 1), 
    Switzerland=(430, 1280, 0.8), 
    Turkey=(975, 1472, 1), 
    Ukraine=(895, 1130, 1), 
    United_Kingdom=(232, 1073, 1)
)
