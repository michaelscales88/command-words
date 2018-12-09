from src import (
    test_speech_recognition, add_training_data, generate_acoustic_features,
    accum_obs_counts, create_mllr_transformation, map_update_model
)
#https://pypi.org/project/pocketsphinx`/

if __name__ == "__main__":
    # Recording your adaptation data
    while str(
        input("Do you want to add training data?")
    )[0].lower() == 'y':
        add_training_data()

    # Adapting the acoustic model
    if str(
        input("Do you want generate acoustic feature files?")
    )[0].lower() == 'y':
        data_set = generate_acoustic_features()
        if data_set:
            accum_obs_counts(data_set)
            create_mllr_transformation(data_set)
            map_update_model(data_set)

    # Test the changes to the acoustic model
    while True:
        cmd = str(input("Do you test the model?"))
        if cmd and cmd[0].lower() == 'y':
            test_speech_recognition()
        else:
            break
