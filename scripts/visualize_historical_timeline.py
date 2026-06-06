import pandas as pd
import matplotlib.pyplot as plt

def visualize_historical_events():
    df = pd.read_csv('data/skinwalker_historical_events.csv')
    df['ds'] = pd.to_datetime(df['ds'])
    
    # Create a categorical scatter plot of events over time
    plt.figure(figsize=(16, 8))
    
    # Group events by sensor type for coloring
    sensors = df['unique_id'].unique()
    colors = plt.cm.get_cmap('tab10', len(sensors))
    
    for i, sensor in enumerate(sensors):
        sensor_df = df[df['unique_id'] == sensor]
        plt.scatter(sensor_df['ds'], [sensor] * len(sensor_df), 
                    s=100, label=sensor, color=colors(i), edgecolors='black')
        
        # Add labels for specific high-value events
        for _, row in sensor_df.iterrows():
            if abs(row['y']) > 100 or 'Travis' in row['label'] or 'Signal' in row['label']:
                plt.annotate(f"{row['label']}\n({row['y']} {row['unit']})", 
                             (row['ds'], sensor),
                             xytext=(5, 5), textcoords='offset points',
                             fontsize=9, alpha=0.8)

    plt.title('Skinwalker Ranch: Historical Anomalous Events Timeline (Verified Reports)', fontsize=14)
    plt.xlabel('Timestamp')
    plt.ylabel('Sensor Channel')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig('data/skinwalker_historical_timeline.png')
    print("Historical event timeline saved to data/skinwalker_historical_timeline.png")

if __name__ == "__main__":
    visualize_historical_events()
