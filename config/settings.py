COLOR_PRESETS = {
    "Ocean": {
        "protein": ["skyblue", "purpleblue", "deepblue", "tv_blue", "blue", "lightblue"],
        "residues": "deepsalmon",
        "interaction_ligand": {
            "C": "greencyan",
            "O": "red", 
            "N": "blue",
            "S": "orange",
            "P": "yellow",
            "H": "white"},
        "surface_ligand": "greencyan"
    },
    "Verdant": {
        "protein": ["limegreen", "chartreuse", "palegreen", "green", "splitpea", "smudge"],
        "residues": "marine",
        "interaction_ligand": {
            "C": "ruby",
            "O": "orange", 
            "N": "blue",
            "S": "orange",
            "P": "yellow",
            "H": "white"
        },
        "surface_ligand": "ruby"
    },
    "Crimson": {
        "protein": ["firebrick", "deepsalmon", "raspberry", "chocolate", "red", "warmpink"],
        "residues": "deepteal",
        "interaction_ligand": {
            "C": "greencyan",
            "O": "red", 
            "N": "blue",
            "S": "orange",
            "P": "yellow",
            "H": "white"
        },
        "surface_ligand": "greencyan"
    },
    "Ash": {
        "protein": ["gray50", "gray70", "white", "palecyan", "bluewhite", "lightblue"],
        "residues": "palegreen",
        "interaction_ligand": {
            "C": "deepteal",
            "O": "red", 
            "N": "blue",
            "S": "orange",
            "P": "yellow",
            "H": "white"
        },
        "surface_ligand": "deepteal"
    },
    "Blossom": {
        "protein": ["warmpink", "purple", "pink", "violet", "raspberry", "violetpurple"],
        "residues": "deepteal",
        "interaction_ligand": {
            "C": "orange",
            "O": "firebrick", 
            "N": "blue",
            "S": "orange",
            "P": "yellow",
            "H": "white"
        },
        "surface_ligand": "orange"
    }
}

EMOJI_MAPPING = {
    "Ocean": "🌊",
    "Verdant": "🌿",
    "Crimson": "🔥",
    "Ash": "🌪️",
    "Blossom": "🌸"
}

EXCLUDED_IONS = {"HOH", "WAT", "SO4", "PO4", "NA", "CL", "CA", "MG", "ZN"}
