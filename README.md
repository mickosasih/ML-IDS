# Intrusion Detection System (IDS) for DoS Attacks using Machine Learning
This project implements an Intrusion Detection System (IDS) using a machine learning approach to detect Denial-of-Service (DoS) attacks based on network traffic bi-directional flow. We use the CICIDS2017 dataset and Python’s CICFlowMeter for real-time packet sniffing capabilities.

## Trained Classifier
The trained classifier employs a Bagging Decision Tree model with nearmiss data balancing to enhance classification performance.

## Getting Started
### Prerequisites
- **Root Access**: To achieve real-time packet sniffing using CICFlowMeter, you'll need root (administrator) privileges to have acces to network interfaces.
- **Python Environment (Recommended)**: We strongly recommend creating a Python virtual environment for this project. This ensures that dependencies are isolated and consistent.
- **Linux Operating System**
### Installation
1. **Clone the Repository:**
   ```
   git clone https://github.com/mickosasih/ML-IDS.git
   ```

2. **Install Requirements:**
   ```
   pip install -r requirements.txt
   ```

3. **Configure CICFlowMeter:**
   - Copy all modified files from the "Modified CICFlowMeter" folder to your installed CICFlowMeter directory.
   - Update the following configuration settings in `app.py`:
     - `ML_API_URL`: Set this to the appropriate URL for your machine learning API.
     - `NETWORK_INTERFACE`: Specify the network interface you want to monitor (e.g., `eth0`, `ens33`).
   - Refer to the [CICFlowMeter repository](https://github.com/hieulw/cicflowmeter) for detailed instructions.
## Usage

## References
1. https://github.com/hieulw/cicflowmeter
2. https://www.unb.ca/cic/datasets/ids-2017.html
3. https://www.unb.ca/cic/research/applications.html#CICFlowMeter
## Disclaimer
This project was developed for research purposes and is not actively maintained. It is not intended for production use without further testing and security considerations.