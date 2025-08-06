# Pocket-Visualizer
🧬 Pocket Visualizer is a Streamlit-powered tool that highlights hydrogen bond interactions in docked protein-ligand complexes and automatically identifies the interacting protein residues.

It leverages PyMOL for high-quality molecular visualization, operating entirely through PyMOL command-line functions, without requiring the PyMOL GUI, to efficiently render and generate publication-ready figures.
Designed for fast-paced workflows, it enables quick, automated analysis of large numbers of complexes with minimal user intervention.

For each input complex, the app:

1. Generates a zoomed-in image of the ligand-binding pocket, showing:

a). Protein-ligand interactions (Hydrogen bonds)

b). Bond lengths

c). Interacting residues

2. 🌐 Creates a surface view image of the complete protein-ligand complex.
3. 💻 Saves PyMOL session files (.pse) for both views.
4. 📄 Outputs a CSV file listing the names and positions of interacting protein residues for each complex.

This tool is ideal for analyzing docking results and gaining insights into molecular interactions in drug discovery workflows.

## **🛠** **Installation**

To run Pocket Visualizer, you need to have the following Python packages installed:
1. Biopython (for parsing protein structure files)
2. PyMOL (for molecular visualization)
3. Streamlit (for the web-based interface)

You can install the required packages as follows:
1. Biopython:

   ```
   pip install biopython
   ```

2. Streamlit:

   ```
   pip install streamlit
   ```

3. PyMOL:

PyMOL is not available via standard `pip` in some environments. You can install it using one of the following methods:

### **Option A:** Using Anaconda (Recommended)

If you're using Anaconda, run:

```
conda install -c schrodinger pymol
```

### **Option B:** Using pip (Open-Source Version)

For the open-source version, you can try:

```
pip install pymol-open-source
```

Note: Ensure that the PyMOL GUI is installed and properly configured if you plan to use the session (.pse) file generation.

### **Option C:** Download from Official Website

You can download the official installer for PyMOL from the Schrödinger website:

🔗 [PyMOL Download](https://www.pymol.org/#download)

After installation, add the PyMOL installation directory to your system's PATH so that it can be accessed from the terminal or command line.

## **📄 Input Requirements**

Please ensure the following conditions are met before using Pocket Visualizer:

🔹 Accepted format: Only `.pdb` (Protein Data Bank) files are supported.

🔹 Each `.pdb` file must contain a single header.

🔹 The app can process a single complex containing upto 6 proteins within a single `.pdb` file.

🔹 Protein chains must be explicitly defined within the `.pdb` file.

🔹 Ligand identifiers must also be correctly annotated in the `.pdb` file.

These requirements ensure correct parsing and accurate visualization of interactions.

## **🎨 Visualization Themes**

Pocket Visualizer offers five pre-defined color themes for customizing the appearance of your protein-ligand complexes:

| Theme       | Description                                      |
| ----------- | ------------------------------------------------ |
| **Ocean**   | Blue-based color palette                         |
| **Verdant** | Green color scheme for a natural look            |
| **Crimson** | Bold red-themed appearance                       |
| **Ash**     | Clean and minimal white theme                    |
| **Blossom** | Vibrant hot pink color palette for eye-catching visualization |

Each theme adjusts molecular surfaces, backgrounds, and highlights to enhance interpretability.

## **🚀 How to Use the App**

1. Navigate to the directory containing the `main.py` file using your terminal or command prompt, then execute the following command to start the app:
```
streamlit run main.py
```

This will launch Pocket Visualizer in your default web browser at `http://localhost:8501/`.
<img width="1920" height="1080" alt="01" src="https://github.com/user-attachments/assets/1fdf4343-b630-481f-9c7a-d90f042f8694" />

2. Specify the input directory where your `.pdb` files are located.
3. Specify the output directory where results will be saved (images, session files, CSV).
4. Select a visualization theme from the available options.
5. Set custom image parameters, including size and DPI.
6. Click "Run Visualizations" to generate figures:
<img width="1920" height="1080" alt="Untitled design" src="https://github.com/user-attachments/assets/172c0d1c-6daf-423f-af43-dacf1d7151f0" />

### For optimal performance, especially with higher resolutions and DPI settings, it's recommended to use a system equipped with a GPU.

## **Rendered Figures:**
<img width="3800" height="3000" alt="03-1A7X-Interactions" src="https://github.com/user-attachments/assets/d9461867-2252-46e3-9e40-4a3a32eb236d" />

<img width="3800" height="3000" alt="03-1A7X-Surface" src="https://github.com/user-attachments/assets/d4a9b33f-07c9-456d-a312-25446e2b4153" />

<img width="3800" height="3000" alt="10" src="https://github.com/user-attachments/assets/2ac3122a-53ed-41e4-9d4a-038c3ede053b" />

<img width="3800" height="3000" alt="9" src="https://github.com/user-attachments/assets/8e5de617-3da5-41ec-ae01-d72e7e0ba829" />

<img width="3800" height="3000" alt="14" src="https://github.com/user-attachments/assets/395a9c56-ac40-4044-b85e-14d50d112442" />

<img width="3800" height="3000" alt="11" src="https://github.com/user-attachments/assets/4a4e5ded-1399-4bb8-bf74-fa8597cbf367" />

<img width="3800" height="3000" alt="05-1A7X-Interactions" src="https://github.com/user-attachments/assets/772c7456-37e7-4bb7-b08f-ef2920453518" />

<img width="3800" height="3000" alt="05-1A52-Surface" src="https://github.com/user-attachments/assets/b5466975-86e6-4d6c-a346-619e5a3a3ed7" />

<img width="3800" height="3000" alt="16" src="https://github.com/user-attachments/assets/0c26a5fd-2e1f-4982-8af9-1248ef12ade0" />

<img width="3800" height="3000" alt="15" src="https://github.com/user-attachments/assets/eb929642-04af-48e5-aff9-5a2ba27c7743" />

## Interacting Residues CSV
<img width="555" height="81" alt="image" src="https://github.com/user-attachments/assets/f60cf0a1-836f-476d-a602-b7fc147665c5" />

It shows interacting protein residue (three letter code) with position followed by the Chain ID.
