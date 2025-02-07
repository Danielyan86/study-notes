![AI-Driven Risk Assessment for Vessel Bioinvasion](https://raw.githubusercontent.com/Danielyan86/images_repo/master/bio-security/Al-Driven%20Risk%20Assessment%20for%20Vessel%20Bioinvasion.png)

### LSTM Autoencoder Architecture

#### Key Components:

- **LSTM**: Handles variable-length sequences with temporal dependencies
- **Autoencoder**: Learns compressed representations through reconstruction
- **Self-supervised Learning**: Trains via input prediction

#### Training:

- **Continuous Features**: MSE/MAE loss, normalized (0-1)
- **Categorical Features**: One-hot encoding, BCE loss, sigmoid activation

### Sequence Encoding

- Transforms voyage sequences into 64-dimensional vectors
- Preserves temporal and spatial patterns

### K-means Clustering

- Input: 64D encoded vectors
- Optimal clusters (k=5) determined by:
  1. Elbow Method
  2. Silhouette Analysis
