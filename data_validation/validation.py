




def validate_filenames(filenames):
    valid_filenames = []
    invalid_filenames = []
    for filename in filenames:
        if '.' in filename:
            invalid_filenames.append(filename)
        else:
            valid_filenames.append(filename)

    return valid_filenames, invalid_filenames

