![AI-Driven Risk Assessment for Vessel Bioinvasion](https://raw.githubusercontent.com/Danielyan86/images_repo/master/bio-security/Al-Driven%20Risk%20Assessment%20for%20Vessel%20Bioinvasion.png)

### Introduction

Global shipping is a major pathway for the spread of non-indigenous species (NIS), posing significant ecological and economic threats to New Zealand's marine ecosystems. Traditional risk profiling frameworks for international vessel arrivals rely on manual interpretation of voyage and maintenance history, resulting in limited accuracy.

This study leverages Automatic Identification System (AIS) data, Marine Bioinvasion Risk Data, and machine learning approaches to develop an automated risk assessment system for vessel bioinvasion.

### Data and Preprocessing

#### Input Data Sources

- **AIS Data**: Historical vessel movements, port visits, and voyage patterns
- **Marine Bioinvasion Risk Data**: Environmental similarity metrics, geographic distance measurements, and latitudinal crossing risk factors

#### Data Processing Pipeline

1. **Data Cleaning**

   - Filter anomalous events
   - Standardize port names
   - Remove duplicate records

2. **Voyage Construction**

   - Define voyage criteria (>2 months duration, >5 port visits)
   - Map vessel paths across geographic regions

3. **Risk Factor Calculation**
   - Compute ecological risk scores using Marine Bioinvasion Risk Data
   - Integrate geographic and environmental factors

### Model Architecture

#### LSTM Autoencoder

1. **Core Components**

   - LSTM layers for processing temporal sequences
   - Encoder-decoder architecture for dimensionality reduction
   - Self-supervised learning approach

2. **Feature Processing**
   - Continuous features: Normalized with MSE/MAE loss
   - Categorical features: One-hot encoded with BCE loss
   - Output: 64-dimensional vector representations

#### Clustering Analysis

- **Method**: K-means clustering on encoded vectors
- **Cluster Optimization**:
  - Determined optimal k=5 using elbow method
  - Validated using silhouette analysis
- **Visualization**: t-SNE for cluster quality assessment

### Results and Analysis

#### Cluster Characteristics

- **High Cohesion Groups** (Clusters 1 & 4)

  - Well-defined vessel movement patterns
  - Clear geographic separation

- **Mixed Pattern Groups** (Clusters 2 & 3)
  - Lower internal consistency
  - Overlapping trajectories

#### Risk Pattern Insights

- **Cross-Regional Patterns**

  - Asia-Australia routes crossing multiple climate zones
  - Environmental transitions affecting species survival

- **Regional Risk Factors**
  - Short-distance Australian routes showing elevated risk
  - Climate zone transitions impacting bioinvasion probability

### Conclusion and Future Directions

#### Achievements

- Successfully developed automated risk assessment system
- Identified distinct vessel movement patterns
- Validated model stability through parameter optimization

#### Future Improvements

1. **Technical Enhancements**

   - Feature engineering optimization
   - Hyperparameter tuning

2. **Domain Integration**
   - Better feature interpretation for practical application
   - Semi-supervised learning with expert knowledge
   - Enhanced validation of clustering results
