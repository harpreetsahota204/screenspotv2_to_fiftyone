# Parsing the ScreenSpot-v2 Dataset to FiftyOne Format



![image/png](screenspot_v2.gif)


This is a [FiftyOne](https://github.com/voxel51/fiftyone) dataset with 1272 samples.

## You can download this dataset directly from Hugging Face

If you haven't already, install FiftyOne:

```bash
pip install -U fiftyone
```

## Usage

```python
import fiftyone as fo
from fiftyone.utils.huggingface import load_from_hub

# Load the dataset
# Note: other available arguments include 'max_samples', etc
dataset = load_from_hub("Voxel51/ScreenSpot-v2")

# Launch the App
session = fo.launch_app(dataset)
```


# Dataset Details
## Dataset Source
- Repository: https://github.com/OS-Copilot/OS-Atlas and https://huggingface.co/datasets/os-copilot/screenspot-v2

- Paper: [OS-ATLAS: A Foundation Action Model for Generalist GUI Agents](https://arxiv.org/abs/2410.23218)

- Project Page: https://osatlas.github.io/

## Uses
### Direct Use
ScreenSpot-V2 is designed for evaluating single-step GUI grounding capabilities across multiple platforms (mobile, desktop, and web). It serves as a benchmark for assessing how well models can locate GUI elements based on natural language instructions.

## Dataset Structure
The dataset is organized by platform type:
- Web domain: 436 questions
- Desktop domain: 334 questions
- Mobile domain: 502 questions

Each question requires identifying either text elements or icon/widget elements based on natural language instructions. The dataset includes screenshots and corresponding ground truth coordinates or bounding boxes for the target elements.

## FiftyOne Dataset Structure

**Basic Info:** 1,581 desktop application screenshots with interaction annotations

**Core Fields:**

- `instruction`: StringField - Natural language task description
- `data_source`: EmbeddedDocumentField(Classification) - Operating system (e.g., "macos")
- `action_detection`: EmbeddedDocumentField(Detection) - Target interaction element:
  - `label`: Element type (e.g., "text", "icon")
  - `bounding_box`: a list of relative bounding box coordinates in [0, 1] in the following format:`[<top-left-x>, <top-left-y>, <width>, <height>]`


## Dataset Creation
### Curation Rationale
ScreenSpot-V2 was created to address annotation errors found in the original ScreenSpot benchmark. The authors identified that approximately 11.32% of the samples contained various issues that could lead to biased evaluation results.

### Source Data
#### Data Collection and Processing
The dataset was derived from the original ScreenSpot benchmark. The authors:
1. Removed problematic questions and replaced them with new ones
2. Revised instructions that were in referring expression grounding (REG) form and rewrote them as natural language instructions
3. Corrected mislabeled ground truth bounding boxes

#### Who are the source data producers?
The OS-ATLAS team, based on the original ScreenSpot benchmark by Cheng et al. (2024)

### Annotations 
#### Annotation process
The authors reviewed the original ScreenSpot dataset, identified problematic samples (approximately 11.32%), and made corrections while maintaining the same total number of questions.

#### Who are the annotators?
The OS-ATLAS research team


## Bias, Risks, and Limitations
The dataset addresses several limitations of the original ScreenSpot benchmark, including:
- Spelling mistakes in instructions
- References to elements not present in screenshots
- Ambiguous questions allowing multiple valid answers
- High similarity between questions
- Incorrectly labeled ground truth bounding boxes

## Recommendations
Users should consider that this dataset is specifically designed for evaluating GUI grounding performance across multiple platforms and may not cover all possible GUI interaction scenarios.

## Citation 
### BibTeX:
```bibtex
@article{wu2024atlas,
        title={OS-ATLAS: A Foundation Action Model for Generalist GUI Agents},
        author={Wu, Zhiyong and Wu, Zhenyu and Xu, Fangzhi and Wang, Yian and Sun, Qiushi and Jia, Chengyou and Cheng, Kanzhi and Ding, Zichen and Chen, Liheng and Liang, Paul Pu and others},
        journal={arXiv preprint arXiv:2410.23218},
        year={2024}
      }
```
### APA:
Wu, Z., Wu, Z., Xu, F., Wang, Y., Sun, Q., Jia, C., Cheng, K., Ding, Z., Chen, L., Liang, P. P., & Qiao, Y. (2024). OS-ATLAS: A foundation action model for generalist GUI agents. arXiv preprint arXiv:2410.23218.
