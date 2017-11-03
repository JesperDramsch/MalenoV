### Function for n-dimensional seismic facies training /classification using Convolutional Neural Nets (CNN)
### By: Charles Rutherford Ildstad (University of Trondheim), as part of a summer intern project in ConocoPhillips and private work
### Contributions from Anders U. Waldeland (University of Oslo), Chris Olsen (ConocoPhillips), Doug Hakkarinen (ConocoPhillips)
### Date: 26.10.2017
### For: ConocoPhillips, Norway,
### GNU V3.0 lesser license

import numpy as np
from keras.models import load_model
import malenov

# Set random seed for reproducability
np.random.seed(42)
# Confirm backend if in doubt
#keras.backend.backend()

#### ---- Run an instance of the master function ----
filedir= 'G:\Code\MalenoV\Dutch F3 seismic data/'
filenames=['multi_facies Prediction_F3_10ep10it_60k_samples.segy']    # name(s) of the segy-cube(s) with data
inp_res = np.float32    # formatting of the input seismic (e.g. np.int8 for 8-bit data, np.float32 for 32-bit data, etc)
cube_incr = 32    # number of increments in each direction to create a training cube
fileloc=[filedir+j for j in filenames]

# Define the dictionary holding all the training parameters

pts_files = ['multi_else_ilxl.pts','multi_grizzly_ilxl.pts','multi_high_amp_continuous_ilxl.pts','multi_high_amplitude_ilxl.pts','multi_low_amp_dips_ilxl.pts','multi_low_amplitude_ilxl.pts','multi_low_coherency_ilxl.pts','multi_salt_ilxl.pts','multi_steep_dips_ilxl.pts']    # list of names of class-adresses

train_dict = {
    'files': [filedir+j for j in pts_files],
    'num_tot_iterations': 25,    # number of times we draw a new training ensemble/mini-batch
    'epochs' : 12,    # number of epochs we run on each training ensemble/mini-batch
    'num_train_ex' : 18000,    # number of training examples in each training ensemble/mini-batch
    'batch_size' : 32,    # number of training examples fed to the optimizer as a batch
    'opt_patience' : 10,    # number of epochs with the same accuracy before force breaking the training ensemble/mini-batch
    'data_augmentation' : False,    # whether or not we are using data augmentation
    'save_model' : True,    # whether or not we are saving the trained model
    'save_location' : filedir+'F3_train'    # file name for the saved trained model
}

# Define the dictionary holding all the prediction parameters
pred_dict = {
    'keras_model' :  load_model(filedir+'Trained model multi_facies_F3_10ep10it_35ksamples.h5'), # input model to be used for prediction, to load a model use: keras.models.load_model('write_location')
    'section_edge' : np.asarray([33282, 33282, 123898, 123900, 128, 2840]), # inline and xline section to be predicted (all depths), must contain xline
    'show_feature' : False,    # Show the distinct features before they are combined to a prediction
    'xline' : 123900,    # xline used for classification (index)(should be within section range)
    'num_class' : len(train_dict['files']),    # number of classes to output
    'cord_syst' : 'segy',    # Coordinate system used, default is 0,0. Set to 'segy' to give inputs in (inline,xline)
    'save_pred' : True,    # Save the prediction as a segy-cube
    'save_location' : filedir+'sunday.segy',     # file name for the saved prediction
    'pred_batch' : 25,     # number of traces used to make batches of mini-cubes that are stored in memory at once
    #'pred_batch' : train_dict['num_train_ex']//(pred_dict['section_edge'][5]-pred_dict['section_edge'][4])    #Suggested value
    'pred_prob' : False     # Give the probabilities of the first class(True), or simply show where each class is classified(False)
}


# Run the master function and save the output in the output dictionary output_dict

output_dict1 = malenov.master(
    segy_filename = fileloc,     # Seismic filenames
    inp_format = inp_res,     # Format of input seismic
    cube_incr = cube_incr,     # Increments in each direction to create a training cube
    train_dict = train_dict,     # Input training dictionary
    pred_dict = pred_dict,     # Input prediction dictionary
    mode = 'predict'     # Input mode ('train', 'predict', or 'full' for both training AND prediction)
)

# Show additional details about the prediciton
#show_details(
#    filename,
#    cube_incr,
#    output_dict['pred'],
#    inline = 100,
#    inl_start = 75,
#    xline = 169,
#    xl_start = 155,
#    slice_number = 400,
#    slice_incr = 3
#)



### Save/load functions
## returns a prediction cube
## identical to the one saved
#prediction = np.load('filename.npy')
#
## returns a compiled model
## identical to the one saved
#loaded_model = keras.models.load_model('filename.h5')
