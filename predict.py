import os
from tensorflow.keras.models import load_model
from clean import downsample_mono, envelope
from kapre.time_frequency import STFT, Magnitude, ApplyFilterbank, MagnitudeToDecibel
from sklearn.preprocessing import LabelEncoder
import numpy as np
from glob import glob
import argparse
import pandas as pd
from tqdm import tqdm
from collections import namedtuple
import pandas as pd


def make_prediction(my_dir):
    model_fn='conv1d.h5'
    pred_fn='y_pred'
    sr=16000
    dt=1.0
    threshold=20


    model = load_model(model_fn,
        custom_objects={'STFT':STFT,
                        'Magnitude':Magnitude,
                        'ApplyFilterbank':ApplyFilterbank,
                        'MagnitudeToDecibel':MagnitudeToDecibel})
    wav_paths = glob('{}/**'.format(my_dir), recursive=True)
    wav_paths = sorted([x.replace(os.sep, '/') for x in wav_paths if '.wav' in x])
    classes = ['Hip Hop', 'House', 'Pop', 'Techno', 'Trap', 'Tropical House']
    results = []
    File = namedtuple('File', 'genreID genre samples dir_path')
    predictions = []

    for z, wav_fn in tqdm(enumerate(wav_paths), total=len(wav_paths)):
        rate, wav = downsample_mono(wav_fn, sr)
        mask, env = envelope(wav, rate, threshold=threshold)
        clean_wav = wav[mask]
        step = int(sr*dt)
        batch = []

        for i in range(0, clean_wav.shape[0], step):
            sample = clean_wav[i:i+step]
            sample = sample.reshape(-1, 1)
            if sample.shape[0] < step:
                tmp = np.zeros(shape=(step, 1), dtype=np.int16)
                tmp[:sample.shape[0],:] = sample.flatten().reshape(-1, 1)
                sample = tmp
            batch.append(sample)
        X_batch = np.array(batch, dtype=np.float32)
        y_pred = model.predict(X_batch)
        y_mean = np.mean(y_pred, axis=0)
        y_pred = np.argmax(y_mean)
        results.append(y_mean)
        file_name = os.path.basename(wav_fn)
        genre = classes[y_pred]
        dir_path = os.path.dirname(wav_fn)
        save_predictions(File, predictions, y_pred, file_name, genre, dir_path)
        
    df = pd.DataFrame(predictions)
    df.to_csv('predictions.csv')
    np.save(pred_fn, np.array(results))
    

def save_predictions(File, predictions, y_pred, samples, genre, file_path):
  predictions.append(File(y_pred, genre, samples, file_path))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Audio Classification Training')
    parser.add_argument('--model_fn', type=str, default='conv1d.h5',
                        help='model file to make predictions')
    parser.add_argument('--pred_fn', type=str, default='y_pred',
                        help='fn to write predictions in logs dir')
    parser.add_argument('--src_dir', type=str, default=my_dir,
                        help='directory containing wavfiles to predict')
    parser.add_argument('--dt', type=float, default=1.0,
                        help='time in seconds to sample audio')
    parser.add_argument('--sr', type=int, default=16000,
                        help='sample rate of clean audio')
    parser.add_argument('--threshold', type=str, default=20,
                        help='threshold magnitude for np.int16 dtype')
    args, _ = parser.parse_known_args()

    make_prediction(args.src_dir)

