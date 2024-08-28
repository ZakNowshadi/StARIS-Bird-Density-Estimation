# Tried to ensure all the hardcoded paths are in one place such that any changes (if needed) can be done easily
# as all the places where these paths are used in the codebase are dependent on these global variables below

global SIMULATION_FRAME_SAVING_FOLDER
SIMULATION_FRAME_SAVING_FOLDER = 'SimulationSavedFrameByFrame'
global MANIPULATED_AUDIO_FOLDER
MANIPULATED_AUDIO_FOLDER = 'Audio/ManipulatedAudioFiles'
global ORIGINAL_AUDIO_FOLDER
ORIGINAL_AUDIO_FOLDER = 'Audio/OriginalAudioFiles'
global SPECIES_IMAGES_FOLDER
SPECIES_IMAGES_FOLDER = 'Images/Species'
global GRAPH_ITEMS_IMAGES_FOLDER
GRAPH_ITEMS_IMAGES_FOLDER = 'Images/GraphItems'
global HOME_IMAGE_FILE
HOME_IMAGE_FILE = GRAPH_ITEMS_IMAGES_FOLDER + '/bird_nest.png'
global TARGET_IMAGE_FILE
TARGET_IMAGE_FILE = GRAPH_ITEMS_IMAGES_FOLDER + '/red_target.png'
# The size of the mask will be a slightly reduced version of the normal graph size
global MASK_MASK_SIZE
MASK_MASK_SIZE = 40
global MAX_GRAPH_SIZE
MAX_GRAPH_SIZE = int(MASK_MASK_SIZE * 1.3)
