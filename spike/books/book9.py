"""Book 9: "Weather". Sun, cloud, rain, wind, snow: what we see and how it feels.
"""
WE = {"pron": "we"}
THE_SKY = {"n": "sky", "art": "the"}
THE_SUN = {"n": "sun", "art": "the"}
SNOW = {"n": "snow", "art": ""}

STORY = {
    "title": "Weather",
    "tense": "pres",
    "cover": {"art": "cover", "clauses": [{"phrase": "title_weather"}]},
    "pages": [
        {"art": "p01_look_sky", "focus": ["look", "sky"],
         "clauses": [{"subj": WE, "verb": "look", "pp": ["at", THE_SKY]}]},
        {"art": "p02_sun_shines", "focus": ["sun"], "clauses": [{"subj": THE_SUN, "verb": "shine", "end": "!"}]},
        {"art": "p03_sun_warm", "focus": ["sun", "warm"], "clauses": [{"subj": THE_SUN, "pred": "warm"}]},
        {"art": "p04_see_cloud", "focus": ["cloud"], "clauses": [{"subj": WE, "verb": "see", "obj": "cloud"}]},
        {"art": "p05_rain_falls", "focus": ["rain"],
         "clauses": [{"subj": {"n": "rain", "art": ""}, "verb": "fall", "end": "!"}]},
        {"art": "p06_grass_wet", "focus": ["grass", "wet"],
         "clauses": [{"subj": {"n": "grass", "art": "the"}, "pred": "wet"}]},
        {"art": "p07_wind_blows", "focus": ["wind"],
         "clauses": [{"subj": {"n": "wind", "art": "the"}, "verb": "blow", "end": "!"}]},
        {"art": "p08_snow_falls", "focus": ["snow"], "clauses": [{"subj": SNOW, "verb": "fall", "end": "!"}]},
        {"art": "p09_snow_cold", "focus": ["snow", "cold"], "clauses": [{"subj": SNOW, "pred": "cold"}]},
        {"art": "p10_look_sky", "focus": ["look", "sky"],
         "clauses": [{"imp": "look", "pp": ["at", THE_SKY], "end": "!"}]},
    ],
}
