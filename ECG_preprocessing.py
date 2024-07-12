import wfdb
import numpy as np
import neurokit2 as nk
from hrvanalysis import remove_outliers, remove_ectopic_beats, interpolate_nan_values
from hrvanalysis import get_time_domain_features
import pandas as pd
#wfdb

def wfdb_to_hrv(db):
    record_list = wfdb.get_record_list(db)
    for rd in record_list:
        record = wfdb.rdrecord('physionet.org/files/{}/1.0.0/{}'.format(db, re))
        signal = record.p_signal[:,0]

        # 노이즈 제거
        ecg = nk.ecg_clean(signal, sampling_rate = record.fs, method='vg')

        # r-peak detection
        rpeaks1 = FastNVG(sampling_frequency=record.fs).find_peaks(ecg)
        rpeaks1_array = np.zeros(len(ecg), dtype=int)
        # rpeaks1에 해당하는 인덱스에 1을 할당합니다.
        rpeaks1_array[rpeaks1] = 1

        # ECG, r-peak
        ecg_rr = np.concatenate([ecg.reshape(-1,1), rpeaks1_array.reshape(-1,1)], axis=1)
        ecg_rr = pd.DataFrame(ecg_rr, columns=['ecg','r'])

        # 1분 간격으로 interval
        for num, i in tqdm(enumerate(range(0, len(ecg_rr), record.fs*60))):
            # 심박변이도는 5분간 측
            ecg_cut = ecg_rr[i:i+record.fs*60*5]

            #이상치 제거 및 심박변이도 계산
            try:
                rr_intervals_without_outliers = remove_outliers(rr_intervals=r_index,  
                                                                    low_rri=300, high_rri=2000)
                # This replace outliers nan values with linear interpolation
                interpolated_rr_intervals = interpolate_nan_values(rr_intervals=rr_intervals_without_outliers,
                                                                   interpolation_method="linear")
    
                # This remove ectopic beats from signal
                nn_intervals_list = remove_ectopic_beats(rr_intervals=interpolated_rr_intervals, method="malik")
                # This replace ectopic beats nan values with linear interpolation
                interpolated_nn_intervals = interpolate_nan_values(rr_intervals=nn_intervals_list)
                time_domain_features = get_time_domain_features(interpolated_nn_intervals)

            except:
                time_domain_features = dict(zip(['mean_nni', 'sdnn', 'sdsd', 'nni_50', 'pnni_50', 'nni_20', 'pnni_20','rmssd', 'median_nni', 'range_nni', 'cvsd', 'cvnni', 'mean_hr','max_hr', 'min_hr', 'std_hr'], 
                                                 [np.NaN for i in range(16)]
                                               )
                                           )
        time_domain_features['time'] = num
        time_domain_features['ID'] = re
        df = pd.DataFrame.from_dict(data=time_domain_features, orient='index').T
        dt = pd.concat([dt, df]).reset_index(drop=True)

        return dt


def custem_data_to_hrv(signal, fs):
    
    # 노이즈 제거
    ecg = nk.ecg_clean(signal, sampling_rate = fs, method='vg')

    # r-peak detection
    rpeaks1 = FastNVG(sampling_frequency=fs).find_peaks(ecg)
    rpeaks1_array = np.zeros(len(ecg), dtype=int)
    # rpeaks1에 해당하는 인덱스에 1을 할당합니다.
    rpeaks1_array[rpeaks1] = 1

    # ECG, r-peak
    ecg_rr = np.concatenate([ecg.reshape(-1,1), rpeaks1_array.reshape(-1,1)], axis=1)
    ecg_rr = pd.DataFrame(ecg_rr, columns=['ecg','r'])

    # 1분 간격으로 interval
    for num, i in tqdm(enumerate(range(0, len(ecg_rr), fs*60))):
        # 심박변이도는 5분간 측
        ecg_cut = ecg_rr[i:i+fs*60*5]

        #이상치 제거 및 심박변이도 계산
        try:
            rr_intervals_without_outliers = remove_outliers(rr_intervals=r_index,  
                                                                low_rri=300, high_rri=2000)
            # This replace outliers nan values with linear interpolation
            interpolated_rr_intervals = interpolate_nan_values(rr_intervals=rr_intervals_without_outliers,
                                                               interpolation_method="linear")

            # This remove ectopic beats from signal
            nn_intervals_list = remove_ectopic_beats(rr_intervals=interpolated_rr_intervals, method="malik")
            # This replace ectopic beats nan values with linear interpolation
            interpolated_nn_intervals = interpolate_nan_values(rr_intervals=nn_intervals_list)
            time_domain_features = get_time_domain_features(interpolated_nn_intervals)

        except:
            time_domain_features = dict(zip(['mean_nni', 'sdnn', 'sdsd', 'nni_50', 'pnni_50', 'nni_20', 'pnni_20','rmssd', 'median_nni', 'range_nni', 'cvsd', 'cvnni', 'mean_hr','max_hr', 'min_hr', 'std_hr'], 
                                             [np.NaN for i in range(16)]
                                           )
                                       )
        time_domain_features['time'] = num
        time_domain_features['ID'] = re
        df = pd.DataFrame.from_dict(data=time_domain_features, orient='index').T
        dt = pd.concat([dt, df]).reset_index(drop=True)

        return dt
