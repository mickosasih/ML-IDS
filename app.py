# Import library
from flask import Flask, request, jsonify, render_template
from skops.io import load
import pandas as pd
import subprocess
import os
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import time
import numpy as np
#Configuration
NETWORK_INTERFACE="ens33"
ML_API_URL= "http://localhost:5000/predict"

app = Flask(__name__)

# Load model
model = load("ml-ids_model.skops", trusted=True)
cicflowmeter_process = None
@app.route('/start-cicflowmeter', methods=['POST'])
def start_cicflowmeter():
    global cicflowmeter_process
    if cicflowmeter_process is None:
        # Start CICFlowMeter
        cicflowmeter_process = subprocess.Popen(['cicflowmeter', '-i', NETWORK_INTERFACE, '-c', 'flow.csv','-u',ML_API_URL])
        return jsonify({'message': 'CICFlowMeter started'}), 200
    else:
        return jsonify({'message': 'CICFlowMeter is already running'}), 200

@app.route('/stop-cicflowmeter', methods=['POST'])
def stop_cicflowmeter():
    global cicflowmeter_process
    if cicflowmeter_process is not None:
        # Terminate CICFlowmeter
        cicflowmeter_process.terminate()
        cicflowmeter_process = None
        return jsonify({'message': 'CICFlowMeter stopped'}), 200
    else:
        return jsonify({'message': 'CICFlowMeter is not running'}), 200


@app.route('/')
def home():
    try:
        df = pd.read_csv("results.csv")

        # Visualisasi results dengan bar chart
        label_counts = df['Label'].value_counts()
        plt.figure(figsize=(8, 6))
        sns.barplot(x=label_counts.index, y=label_counts.values, palette='viridis')
        plt.xlabel('Label')
        plt.ylabel('Count')
        plt.title('Results')
        plt.show()

        # Save image
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        mean_value = np.round((np.mean(df['Predict Execution Time'])*1000),decimals=2)
        max_value = np.round((np.max(df['Predict Execution Time'])*1000),decimals=2)
        min_value = np.round((np.min(df['Predict Execution Time'])*1000),decimals=2)
        return render_template('index.html',plot_url=plot_url,records=df.to_dict('records'),mean=mean_value,max=max_value,min=min_value)
    except Exception as e:
        print(f"Error loading DataFrame: {e}")
        return render_template('index.html')

   



@app.route('/predict', methods=['POST'])
def predict():
    try:
        start_time = time.perf_counter()
        # Ambil data dari CICFlowMeter
        columns = request.json['columns']
        data = request.json['data']
        # Process data ke dataframe
        df = pd.DataFrame(data, columns=columns)
        temp = df[["src_ip", "dst_ip", "src_port", "protocol", "timestamp"]]
        df.drop(columns=['src_ip', 'dst_ip', 'src_port', 'protocol', 'timestamp'], inplace=True)
        column_order = [
            ' Destination Port',
            ' Flow Duration',
            ' Total Fwd Packets',
            ' Total Backward Packets',
            'Total Length of Fwd Packets',
            ' Total Length of Bwd Packets',
            ' Fwd Packet Length Max',
            ' Fwd Packet Length Min',
            ' Fwd Packet Length Mean',
            ' Fwd Packet Length Std',
            'Bwd Packet Length Max',
            ' Bwd Packet Length Min',
            ' Bwd Packet Length Mean',
            ' Bwd Packet Length Std',
            'Flow Bytes/s',
            ' Flow Packets/s',
            ' Flow IAT Mean',
            ' Flow IAT Std',
            ' Flow IAT Max',
            ' Flow IAT Min',
            'Fwd IAT Total',
            ' Fwd IAT Mean',
            ' Fwd IAT Std',
            ' Fwd IAT Max',
            ' Fwd IAT Min',
            'Bwd IAT Total',
            ' Bwd IAT Mean',
            ' Bwd IAT Std',
            ' Bwd IAT Max',
            ' Bwd IAT Min',
            'Fwd PSH Flags',
            ' Bwd PSH Flags',
            ' Fwd URG Flags',
            ' Bwd URG Flags',
            ' Fwd Header Length',
            ' Bwd Header Length',
            'Fwd Packets/s',
            ' Bwd Packets/s',
            ' Min Packet Length',
            ' Max Packet Length',
            ' Packet Length Mean',
            ' Packet Length Std',
            ' Packet Length Variance',
            'FIN Flag Count',
            ' SYN Flag Count',
            ' RST Flag Count',
            ' PSH Flag Count',
            ' ACK Flag Count',
            ' URG Flag Count',
            ' CWE Flag Count',
            ' ECE Flag Count',
            ' Down/Up Ratio',
            ' Average Packet Size',
            ' Avg Fwd Segment Size',
            ' Avg Bwd Segment Size',
            'Fwd Avg Bytes/Bulk',
            ' Fwd Avg Packets/Bulk',
            ' Fwd Avg Bulk Rate',
            ' Bwd Avg Bytes/Bulk',
            ' Bwd Avg Packets/Bulk',
            'Bwd Avg Bulk Rate',
            'Subflow Fwd Packets',
            ' Subflow Fwd Bytes',
            ' Subflow Bwd Packets',
            ' Subflow Bwd Bytes',
            'Init_Win_bytes_forward',
            ' Init_Win_bytes_backward',
            ' act_data_pkt_fwd',
            ' min_seg_size_forward',
            'Active Mean',
            ' Active Std',
            ' Active Max',
            ' Active Min',
            'Idle Mean',
            ' Idle Std',
            ' Idle Max',
            ' Idle Min'
        ]
        df.rename(columns={
            'dst_port': ' Destination Port',
            'flow_duration': ' Flow Duration',
            'flow_byts_s': 'Flow Bytes/s',
            'flow_pkts_s': ' Flow Packets/s',
            'fwd_pkts_s': 'Fwd Packets/s',
            'bwd_pkts_s': ' Bwd Packets/s',
            'tot_fwd_pkts': ' Total Fwd Packets',
            'tot_bwd_pkts': ' Total Backward Packets',
            'totlen_fwd_pkts': 'Total Length of Fwd Packets',
            'totlen_bwd_pkts': ' Total Length of Bwd Packets',
            'fwd_pkt_len_max': ' Fwd Packet Length Max',
            'fwd_pkt_len_min': ' Fwd Packet Length Min',
            'fwd_pkt_len_mean': ' Fwd Packet Length Mean',
            'fwd_pkt_len_std': ' Fwd Packet Length Std',
            'bwd_pkt_len_max': 'Bwd Packet Length Max',
            'bwd_pkt_len_min': ' Bwd Packet Length Min',
            'bwd_pkt_len_mean': ' Bwd Packet Length Mean',
            'bwd_pkt_len_std': ' Bwd Packet Length Std',
            'pkt_len_max': ' Max Packet Length',
            'pkt_len_min': ' Min Packet Length',
            'pkt_len_mean': ' Packet Length Mean',
            'pkt_len_std': ' Packet Length Std',
            'pkt_len_var': ' Packet Length Variance',
            'fwd_header_len': ' Fwd Header Length',
            'bwd_header_len': ' Bwd Header Length',
            'fwd_seg_size_min': ' min_seg_size_forward',
            'fwd_act_data_pkts': ' act_data_pkt_fwd',
            'flow_iat_mean': ' Flow IAT Mean',
            'flow_iat_max': ' Flow IAT Max',
            'flow_iat_min': ' Flow IAT Min',
            'flow_iat_std': ' Flow IAT Std',
            'fwd_iat_tot': 'Fwd IAT Total',
            'fwd_iat_max': ' Fwd IAT Max',
            'fwd_iat_min': ' Fwd IAT Min',
            'fwd_iat_mean': ' Fwd IAT Mean',
            'fwd_iat_std': ' Fwd IAT Std',
            'bwd_iat_tot': 'Bwd IAT Total',
            'bwd_iat_max': ' Bwd IAT Max',
            'bwd_iat_min': ' Bwd IAT Min',
            'bwd_iat_mean': ' Bwd IAT Mean',
            'bwd_iat_std': ' Bwd IAT Std',
            'fwd_psh_flags': 'Fwd PSH Flags',
            'bwd_psh_flags': ' Bwd PSH Flags',
            'fwd_urg_flags': ' Fwd URG Flags',
            'bwd_urg_flags': ' Bwd URG Flags',
            'fin_flag_cnt': 'FIN Flag Count',
            'syn_flag_cnt': ' SYN Flag Count',
            'rst_flag_cnt': ' RST Flag Count',
            'psh_flag_cnt': ' PSH Flag Count',
            'ack_flag_cnt': ' ACK Flag Count',
            'urg_flag_cnt': ' URG Flag Count',
            'ece_flag_cnt': ' ECE Flag Count',
            'down_up_ratio': ' Down/Up Ratio',
            'pkt_size_avg': ' Average Packet Size',
            'init_fwd_win_byts': 'Init_Win_bytes_forward',
            'init_bwd_win_byts': ' Init_Win_bytes_backward',
            'active_max': ' Active Max',
            'active_min': ' Active Min',
            'active_mean': 'Active Mean',
            'active_std': ' Active Std',
            'idle_max': ' Idle Max',
            'idle_min': ' Idle Min',
            'idle_mean': 'Idle Mean',
            'idle_std': ' Idle Std',
            'fwd_byts_b_avg': 'Fwd Avg Bytes/Bulk',
            'fwd_pkts_b_avg': ' Fwd Avg Packets/Bulk',
            'bwd_byts_b_avg': ' Bwd Avg Bytes/Bulk',
            'bwd_pkts_b_avg': ' Bwd Avg Packets/Bulk',
            'fwd_blk_rate_avg': ' Fwd Avg Bulk Rate',
            'bwd_blk_rate_avg': 'Bwd Avg Bulk Rate',
            'fwd_seg_size_avg': ' Avg Fwd Segment Size',
            'bwd_seg_size_avg': ' Avg Bwd Segment Size',
            'cwe_flag_count': ' CWE Flag Count',
            'subflow_fwd_pkts': 'Subflow Fwd Packets',
            'subflow_bwd_pkts': ' Subflow Bwd Packets',
            'subflow_fwd_byts': ' Subflow Fwd Bytes',
            'subflow_bwd_byts': ' Subflow Bwd Bytes'
        }, inplace=True)
        df = df[column_order]
        # Predict
        prediction = model.predict(df)
        probability = pd.DataFrame(model.predict_proba(df), columns=[f'{cls}' for cls in model.classes_])
        df["Label"] = prediction
        df["Probability"] = probability[prediction]*100
        end_time = time.perf_counter()
        df["Predict Execution Time"] = end_time-start_time
        full_df = pd.concat([temp,df],axis=1)
        # Export dataframe ke csv
        if not os.path.isfile("results.csv"):
            full_df.to_csv("results.csv", header=True, index=False)
        else:
            full_df.to_csv("results.csv", mode='a', header=False, index=False)
        return jsonify({'data': data, 'columns': columns})
    except KeyError:
        return jsonify({'error': 'Invalid JSON data'})

if __name__ == '__main__':
    app.run(debug=True)
