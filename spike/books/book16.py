"""Book 16: "Clap! Stomp! Hooray!" — the action song "If You're Happy and You Know It".

Russian: «Если весело живёшь», the song every Russian child knows. Three verses (clap, stomp,
hooray) with the same refrain each time, then a finale that chains all three actions. The verse
lines are recitation pages (no cards, bigger text); the action pages carry the word card.
"""


STORY = {
    "title": "Clap! Stomp! Hooray!",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_happy_song"}]},
    "pages": [
        {"art": "p01_happy_clap",  # the refrain: a recitation page
         "clauses": [{"phrase": "happy_clap"}]},
        {"art": "p02_clap", "focus": ["clap"],
         "clauses": [{"phrase": "clap_go"}]},
        {"art": "p03_happy_stomp",
         "clauses": [{"phrase": "happy_stomp"}]},
        {"art": "p04_stomp", "focus": ["stomp"],
         "clauses": [{"phrase": "stomp_go"}]},
        {"art": "p05_happy_hooray",
         "clauses": [{"phrase": "happy_hooray"}]},
        {"art": "p06_hooray",
         "clauses": [{"phrase": "hooray_go"}]},
        {"art": "p07_happy_all",
         "clauses": [{"phrase": "happy_all"}]},
        {"art": "p08_all_three", "focus": ["clap", "stomp"],  # the finale: all three actions
         "clauses": [{"phrase": "title_happy_song"}]},
    ],
}
