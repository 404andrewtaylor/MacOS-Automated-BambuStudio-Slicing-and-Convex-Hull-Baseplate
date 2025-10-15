# STL to Hull Baseplate Pipeline - How to Use Guide

## 🚀 Quick Start

### Prerequisites
- **macOS** (required for Bambu Studio automation)
- **Bambu Studio** installed in `/Applications/BambuStudio.app`
- **Python 3.6+** installed
- **Terminal access** with proper permissions

### ⚠️ IMPORTANT: Bambu Studio Setup (Required Before Running)

**You MUST complete this setup before running the pipeline:**

1. **Open Bambu Studio**
2. **Create a new project** (File → New Project)
3. **Configure your preferred settings:**
   - Select your printer model
   - Choose your filament type and color
   - Set all your preferred print settings (layer height, infill, supports, etc.)
   - Configure any other settings you want to use
4. **Save this empty project** (File → Save As)
   - Save it anywhere (the location doesn't matter)
   - This ensures Bambu Studio opens with your preferred settings

**Why this is critical:** The automation will open Bambu Studio and use whatever settings are currently active. Without this setup, it will use default settings that may not be suitable for your printer/filament.

### One-Time Setup

1. **Navigate to the pipeline directory:**
   ```bash
   cd /path/to/pipeline_scripts
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Grant Terminal accessibility permissions:**
   - Open **System Preferences** → **Security & Privacy** → **Privacy** → **Accessibility**
   - Add **Terminal** to the list and check the box
   - Restart Terminal if needed

### Running the Pipeline

**Basic Usage:**
```bash
./full_pipeline.sh "/path/to/your/model.stl"
```

**Example:**
```bash
./full_pipeline.sh "/path/to/your/model.stl"
```

## 📋 What the Pipeline Does

The pipeline automatically performs these steps:

1. **Slices the original STL** in Bambu Studio
2. **Extracts the convex hull** from the first layer
3. **Creates a 1mm extruded hull STL**
4. **Calculates alignment offset** and moves the hull to match the original position
5. **Slices the aligned hull** in Bambu Studio
6. **Combines the hull baseplate** with the original model using ReplaceBaseplate
7. **Organizes all output files** and creates analysis reports

## 📁 Output Files

The pipeline creates a folder named `{model_name}_pipeline` containing:

### Main Output Files
- **`{model_name}_with_hull_baseplate.gcode.3mf`** - **Final combined model ready for 3D printing**
- `{model_name}.gcode.3mf` - Original sliced model
- `{model_name}_hull.stl` - Extruded convex hull STL
- `{model_name}_hull.gcode.3mf` - Sliced and aligned hull
- `{model_name}_hull.3mf` - Hull project file

### Analysis Files
- `hull_points.txt` - Hull vertices for reference
- `first_layer_analysis.png` - Visualization of first layer
- `pipeline_summary.txt` - Complete pipeline report

## 🔧 Troubleshooting

### Common Issues

**1. "osascript is not allowed to send keystrokes" Error**
- **Solution:** Grant Terminal accessibility permissions in System Preferences
- Go to Security & Privacy → Privacy → Accessibility
- Add Terminal and check the box
- Restart Terminal

**2. "Bambu Studio not found" Error**
- **Solution:** Install Bambu Studio in `/Applications/BambuStudio.app`
- Download from: https://bambulab.com/en/download/studio

**3. Permission Errors**
- **Solution:** Make scripts executable
  ```bash
  chmod +x *.sh
  ```

**4. Python Dependencies Missing**
- **Solution:** Run setup script again
  ```bash
  ./setup.sh
  ```

### Manual Steps (If Automation Fails)

If the AppleScript automation fails, you can complete the pipeline manually:

1. **Open Bambu Studio**
2. **Import your STL** (Cmd+I)
3. **Slice the model** (Cmd+R)
4. **Export as .gcode.3mf** (Cmd+G)
5. **Save the project** (Cmd+S)

The pipeline will detect the generated files and continue automatically.

### ⚠️ Known Issue: Filament Sync Popup

**Sometimes Bambu Studio will show a popup asking to sync filament settings between importing and slicing.**

**What to do:**
- **Be ready to act quickly** - you have only a few seconds
- **Click "Sync Now"** as soon as the popup appears
- **You may need to click it multiple times** if there are multiple prompts
- **The automation will continue** once you handle the popup

**Why this happens:** Bambu Studio sometimes detects that the filament settings need to be synchronized with the cloud or printer.

**Future improvement:** This is a known limitation that may be addressed in future versions of the pipeline.

## 📊 Understanding the Results

### Hull Metrics
- **Area:** Total area of the convex hull baseplate
- **Perimeter:** Length of the hull boundary
- **Dimensions:** Width x Height of the hull
- **Center:** X,Y coordinates of the hull center
- **Vertices:** Number of points defining the hull shape

### Layer Replacement
- The pipeline replaces the bottom 5 layers of your original model
- These layers are replaced with the convex hull baseplate
- The hull provides a stable, flat foundation for printing

## 🎯 Best Practices

### Input STL Requirements
- **Watertight mesh** (no holes or gaps)
- **Proper orientation** (base should be flat on build plate)
- **Reasonable size** (fits within Bambu Studio's build volume)

### Output Usage
- **Print the final combined model** (`*_with_hull_baseplate.gcode.3mf`)
- **Use standard print settings** (the hull is designed to print easily)
- **The hull baseplate provides excellent bed adhesion**

## 🔍 Advanced Usage

### Customizing Hull Height
Edit `hull_to_stl.py` and change the `extrusion_height` variable:
```python
extrusion_height = 1.0  # Change this value (in mm)
```

### Adjusting Layer Replacement
Edit `ReplaceBaseplate/replace_baseplate_layers.py` and modify:
```python
layers_to_replace = 5  # Change number of layers to replace
```

### Batch Processing
Create a script to process multiple STL files:
```bash
#!/bin/bash
for stl_file in /path/to/stl/files/*.stl; do
    ./full_pipeline.sh "$stl_file"
done
```

## 📞 Support

If you encounter issues:

1. **Check the pipeline summary** in the output directory
2. **Verify all prerequisites** are installed
3. **Check Terminal permissions** in System Preferences
4. **Review the generated analysis files** for insights

## 🎉 Success!

When the pipeline completes successfully, you'll see:
```
🎉 Full Pipeline Completed Successfully!
📁 All files saved to: {output_directory}
🚀 Ready for 3D printing both the original and hull models!
```

Your final printable file is `{model_name}_with_hull_baseplate.gcode.3mf` - load this into Bambu Studio and print!

---

**Created:** October 14, 2025  
**Pipeline Version:** 1.0  
**Tested on:** macOS with Bambu Studio
