---
layout: default
title: Cilia Analysis
author: Herrington, Kari
---

# Cilia Analysis

We have had a number of people analyze Cilia in the Core and ask us
questions about how to analyze their cilia, primarily in terms of
segmenting then measuring


### NIS Elements

- A popular method inspired by this
 paper: [https://pmc.ncbi.nlm.nih.gov/articles/PMC8791558/](https://pmc.ncbi.nlm.nih.gov/articles/PMC8791558/)
- Easy to use and get set up on
- The basics is to Train with the Elements Ai (pixel-based machine
 learning), then analyze with a pipeline in the software
- Great for segmenting in 2D or 3D, then measuring fluorescence/size and shape
- NOTE: Steps acquiring on  a microscope that uses micro-manager for easier import/NIS Elements
   - Capture stacks using the relative method instead of absolute
   - Save as tiff sequence (can also save as ome.tiff if preffered and run a macro to convert if you don't mind the extra step)
   - Use the Converting tiff seq to ND2 PDF below to get your images in to NIS-elements
<details>
<summary><strong>📄 Converting tiff seq to ND2 </strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdfDataAnalysis/Convert Image Seq to ND2.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/GeneralQuickstart/Auto White for Color Imaging in Elements.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

### CiliaQ

- [CiliaQ: a simple, open-source software for automated quantification
 of ciliary morphology and fluorescence in 2D, 3D, and 4D images -
 PubMed](https://pubmed.ncbi.nlm.nih.gov/33683488/ "https://pubmed.ncbi.nlm.nih.gov/33683488/")
- Recommended by our specialist Micaela Lasser who used it in her
 paper! [Ciliary biology intersects autism and congenital heart
 disease -
 PubMed](https://pubmed.ncbi.nlm.nih.gov/39131273/ "https://pubmed.ncbi.nlm.nih.gov/39131273/")



