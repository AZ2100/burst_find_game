import csv, os, sys, pickle


def load_data(path_to_files="game_data"):
    if not os.path.isdir(path_to_files):
        path_to_files = os.path.join("..", "game_data")
        if not os.path.isdir(path_to_files):
            path_to_files = "game_data"
            if not os.path.isdir(path_to_files):
                print("COULD NOT FIND PATH TO FILES")
                sys.exit()
    out_folder = os.path.join(os.path.dirname(path_to_files), "out_files")
    safe_folder(out_folder)

    data = []
    for subject in sorted(os.listdir(path_to_files)):
        subj_path = os.path.join(path_to_files, subject)
        if not os.path.isdir(subj_path):
            continue

        out_sub_folder = os.path.join(out_folder, subject)
        safe_folder(out_sub_folder)
        for subj_data in os.listdir(subj_path):
            if subj_data[-2:] == ".p":
                sub_data = pickle.load(open(os.path.join(subj_path, subj_data)))
                for i, signal in enumerate(sub_data["signals"]):
                    out_signal_folder = os.path.join(out_sub_folder, "signal_"+str(i))
                    signal_dict = {"root_path": subj_path, "title": subject, "out_path": out_signal_folder,
                                   "local_n": i, "global_n": len(data), "calculated_segments": sub_data["segments"][i],
                                   "signal": signal, "df_f": sub_data["df_f"][i]}
                    data.append(signal_dict)
                break
    return data


def csv_save(signals, file_path):
    safe_folder(os.path.dirname(file_path))
    with open(file_path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(signals)


def save_string(line, file_path):
    with open(file_path, "a") as f:
        f.write(line + '\n')


def safe_folder(folder):
    """Checks if folder exists and if it does not creates the folder"""
    if not os.path.exists(folder):
        os.makedirs(folder)