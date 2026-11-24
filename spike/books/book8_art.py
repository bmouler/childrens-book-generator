"""Book 8 art prompts: Animal Sounds. The page names match the `art` keys of book8.py."""

WAVES = "exactly three short curved dark-navy sound-wave arcs, nested like ripples, getting bigger outward"
NO_EXTRA = "There are no music notes, no speech bubbles, no hearts, no stars and no sparkles."
NO_ANIMAL = "There is no animal, no bird and no other person in the picture, only the toddler."
REAL = "drawn like a real animal with natural proportions, standing on four legs, with no clothes"
DOG = "one friendly brown-and-white dog with floppy ears"
CAT = "one orange cat"
DUCK = "one yellow duck with an orange beak and orange webbed feet"
COW = "one black-and-white cow with small horns and a pink nose"

PAGES = {
    "p01_listen": f"Show the same toddler from the reference picture standing and facing the viewer, cupping one hand behind one ear, head tilted to the side, eyes wide, listening carefully with a closed calm mouth. The picture shows only the toddler on a plain pale background. There are no sound-wave lines. {NO_ANIMAL} {NO_EXTRA}",
    "p02_who_barks": f"Show the same toddler from the reference picture standing on the left half of the picture, turned toward the right, cupping one hand behind one ear and looking toward the right edge of the picture with curious wide eyes. In the empty air on the right side of the picture, close to the right edge but well inside it, float {WAVES}, opening toward the toddler, as if a sound comes from outside the picture. {NO_ANIMAL} {NO_EXTRA}",
    "p03_dog_barks": f"Show the same toddler from the reference picture standing on the left and smiling, next to {DOG} on the right, {REAL}. The dog faces the toddler side-on with its mouth open, barking. Directly in front of the dog's open mouth float {WAVES}. There is only one dog and only one toddler in the picture. {NO_EXTRA}",
    "p04_who_meows": f"Show the same toddler from the reference picture sitting on the floor on the right half of the picture, turned toward the left, cupping both hands behind both ears and looking toward the left edge of the picture with a surprised round mouth. In the empty air on the left side of the picture, close to the left edge but well inside it, float {WAVES}, opening toward the toddler, as if a sound comes from outside the picture. {NO_ANIMAL} {NO_EXTRA}",
    "p05_cat_meows": f"Show the same toddler from the reference picture sitting on the floor on the left with crossed legs and a gentle smile, next to {CAT} on the right, drawn like a real cat with natural proportions and no clothes. The cat sits upright on its back legs with its front paws together on the floor, its head turned up and its mouth open, meowing. The cat is small, its head is lower than the toddler's shoulder. Directly in front of the cat's open mouth float {WAVES}, small. There is only one cat and only one toddler in the picture. {NO_EXTRA}",
    "p06_who_moos": f"Show the same toddler from the reference picture standing on tiptoes in the lower left part of the picture, stretching up, with one hand cupped behind one ear and the head tipped back, looking up toward the top right corner of the picture. In the empty air in the upper right part of the picture, near the top right corner but well inside it, float {WAVES}, opening toward the toddler, as if a sound comes from outside the picture. {NO_ANIMAL} {NO_EXTRA}",
    "p07_cow_moos": f"Show the same toddler from the reference picture standing on the left and looking up in wonder at {COW} standing on the right, {REAL}. The cow is seen from the side and is much bigger than the toddler: the cow's back is far above the toddler's head. The cow has its head turned toward the toddler and its mouth open, mooing. Directly in front of the cow's open mouth float {WAVES}. The whole cow, with all four hooves, its tail and its horns, is inside the picture with empty space around it. There is only one cow and only one toddler in the picture. {NO_EXTRA}",
    "p08_who_quacks": f"Show the same toddler from the reference picture crouching low on the left half of the picture, knees bent, with one hand cupped behind one ear, looking down and toward the lower right of the picture with curious wide eyes. In the empty air near the floor on the right side of the picture, close to the right edge but well inside it, float {WAVES}, small, opening toward the toddler, as if a sound comes from outside the picture. {NO_ANIMAL} {NO_EXTRA}",
    "p09_duck_quacks": f"Show the same toddler from the reference picture standing on the left and smiling, looking down at {DUCK} standing on the floor on the right, drawn like a real duck with natural proportions, two legs and no clothes. The duck reaches up to the toddler's knee. The duck faces the toddler with its orange beak wide open, quacking. Directly in front of the duck's open beak float {WAVES}, small. There is only one duck and only one toddler in the picture. There is no water. {NO_EXTRA}",
    "p10_now_you": f"Show the same toddler from the reference picture standing and facing the viewer, joyful, with both hands cupped around the open mouth like a little megaphone, calling out loud with the mouth wide open. Directly in front of the toddler's mouth, to one side of the face, float {WAVES}. {NO_ANIMAL} {NO_EXTRA}",
}
COVER = (
    f"Show the same toddler from the reference picture standing in the middle of the picture, facing the viewer "
    f"and smiling. On the floor at the toddler's left side sits {DOG}. On the floor at the toddler's right side "
    f"sits {CAT}. On the floor in front of the toddler's feet stands {DUCK}. All three animals are drawn like real "
    f"animals with natural proportions and no clothes, with closed mouths, and they are smaller than the toddler. "
    f"There is exactly one dog, exactly one cat, exactly one duck and only one toddler in the picture, and no other "
    f"animal. There are no sound-wave lines. {NO_EXTRA}"
)
