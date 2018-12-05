from src import test_speech_recognition, add_training_data, generate_acoustic_features
#https://pypi.org/project/pocketsphinx`/

if __name__ == "__main__":
    # Recording your adaptation data
    while str(
        input("Do you want to add training data?")
    )[0].lower() == 'y':
        add_training_data()
    # Adapting the acoustic model
    while str(
        input("Do you want generate acoustic feature files?")
    )[0].lower() == 'y':
        generate_acoustic_features()
    # Test the changes to the acoustic model
    while str(
        input("Do you want generate acoustic feature files?")
    )[0].lower() == 'y':
        test_speech_recognition()
        pass
