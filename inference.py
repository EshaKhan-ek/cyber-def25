# inference.py
import os, glob, joblib, pandas as pd
 
MODEL_PATH  = '/app/model.pkl'
INPUT_DIR   = '/input/logs'
OUTPUT_FILE = '/output/alerts.csv'
 
def load_model():
    model = joblib.load(MODEL_PATH)
    print(f'[INFO] Model loaded from {MODEL_PATH}')
    return model
 
def parse_log(filepath):
    """Parse a CSV-formatted network log into a DataFrame."""
    df = pd.read_csv(filepath)
    return df
 
def run_inference(model, df):
    """Run prediction and attach labels to the dataframe."""
    predictions = model.predict(df)
    df['threat'] = predictions
    return df[df['threat'] == 1]  # Return only detected threats
 
def main():
    model = load_model()
    os.makedirs('/output', exist_ok=True)
    all_alerts = []
 
    log_files = glob.glob(os.path.join(INPUT_DIR, '*.log'))
    if not log_files:
        print('[WARN] No log files found in /input/logs')
        return
 
    for log_file in log_files:
        print(f'[INFO] Analyzing {log_file}...')
        df = parse_log(log_file)
        alerts = run_inference(model, df)
        if not alerts.empty:
            alerts['source_file'] = os.path.basename(log_file)
            all_alerts.append(alerts)
 
    if all_alerts:
        result = pd.concat(all_alerts, ignore_index=True)
        result.to_csv(OUTPUT_FILE, index=False)
        print(f'[DONE] {len(result)} threats detected. Alerts saved to {OUTPUT_FILE}')
    else:
        print('[DONE] No threats detected in any log file.')
 
if __name__ == '__main__':
    main()
