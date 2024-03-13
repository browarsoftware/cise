import numpy as np
dim_count = 62
path_to_results = 'data'
emb_array = np.load(path_to_results + "/emb_array_wybrane_3600.npy")
emb_array = emb_array[:, 0:dim_count]
with open(path_to_results + '/embedding.npy', 'wb') as f:
    np.save(f, emb_array)

how_many_images = 573335
v_correct = np.load(path_to_results + "//v_st_" + str(how_many_images) + ".npy")[:,0:dim_count]
with open(path_to_results + '/v_st.npy', 'wb') as f:
    np.save(f, v_correct)
