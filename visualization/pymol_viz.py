import os
from collections import defaultdict
from itertools import cycle
from Bio import PDB
from pymol import cmd
from config.settings import COLOR_PRESETS, EXCLUDED_IONS
from data_handling.file_io import write_interacting_residues_csv

def classify_residues(pdb_file):
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure("complex", pdb_file)
    
    protein_chains = defaultdict(set)
    ligand_residues = set()
    
    for model in structure:
        for chain in model:
            for residue in chain:
                resname = residue.resname.strip()
                is_hetatm = residue.id[0].strip() != ''
                
                if PDB.is_aa(residue):
                    protein_chains[chain.id].add(residue.id[1])
                elif resname in {"UNK", "UNL"}:
                    ligand_residues.add((chain.id, resname, residue.id[1]))
                elif is_hetatm and resname not in EXCLUDED_IONS:
                    ligand_residues.add((chain.id, resname, residue.id[1]))
    
    return protein_chains, ligand_residues

def separate_protein_ligand(pdb_file, output_dir):
    protein_chains, ligand_res = classify_residues(pdb_file)
    
    try:
        cmd.load(pdb_file, "complex")
        cmd.remove(" or ".join([f"resn {res}" for res in EXCLUDED_IONS]))
        
        for chain_id, res_ids in protein_chains.items():
            sel_name = f"protein_{chain_id}"
            resi_clause = "+".join(str(rid) for rid in res_ids)
            cmd.select(sel_name, f"complex and chain {chain_id} and resi {resi_clause}")
        
        ligand_sel = " or ".join(
            [f"(chain {c} and resn {rn} and resi {rid})" for (c, rn, rid) in ligand_res]
        )
        cmd.select("ligand", f"complex and ({ligand_sel})")
        
        return True
    
    except Exception as e:
        return False

def visualize_interactions(pdb_file, output_dir, protein_color, ligand_colors, residues_color,
                           width, height, dpi):
    if not separate_protein_ligand(pdb_file, output_dir):
        return None, None
    
    try:
        cmd.bg_color("white")
        protein_selections = [name for name in cmd.get_names('selections') 
                            if name.startswith('protein_')]
        
        color_pool = cycle(COLOR_PRESETS[protein_color]["protein"])
        for chain_sel in protein_selections:
            cmd.color(next(color_pool), chain_sel)
            cmd.show("cartoon", chain_sel)
            cmd.set("cartoon_fancy_helices", 1)

        for element, color in ligand_colors.items():
            cmd.color(color, f"ligand and elem {element}")

        cmd.show("sticks", "ligand")
        cmd.show("spheres", "ligand")
        cmd.set("sphere_scale", 0.23)
        
        cmd.set('ray_trace_mode', 3)
        cmd.set('ray_trace_gain', 0.6)
        cmd.set('ambient', 0.3)
        cmd.set("direct", 0.6)
        cmd.set('specular', 0.2)
        cmd.set('shininess', 200)
        cmd.set('depth_cue', 0)
        cmd.set('cartoon_highlight_color', 'grey35')
        cmd.set("ray_shadow", 1)
        cmd.set('antialias', 4)
        
        cmd.select("proteins", " or ".join(protein_selections))
        cmd.distance("hbonds", "(proteins and (donor or acceptor))", "(ligand and (donor or acceptor))", mode=2)
        cmd.distance("prot_bonds", "(proteins and donor)", "(ligand and acceptor)", mode=2)
        cmd.distance("lig_bonds", "(proteins and acceptor)", "(ligand and donor)", mode=2)
        cmd.select("prot_donor", "proteins and donor")
        cmd.select("lig_accept", "ligand and acceptor")
        cmd.distance("polar_contacts", "prot_donor", "lig_accept", mode=3, cutoff=3.5)
        cmd.color("yellow", "polar_contacts")
        cmd.show("dashes", "hbonds")
        cmd.color("yellow", "hbonds")
        cmd.select("prot_accept", "proteins and acceptor")
        cmd.select("lig_donor", "ligand and donor")
        cmd.distance("contacts", "prot_accept", "lig_donor", mode=3, cutoff=3.5)
        cmd.select("hb_donors", "(proteins and donor) within 3.5 of (ligand and acceptor)")
        cmd.select("hb_acceptors", "(proteins and acceptor) within 3.5 of (ligand and donor)")
        cmd.select("hb_residues", "byres hb_donors or hb_acceptors")
        cmd.show("sticks", "hb_residues")
        cmd.color(residues_color, "hb_residues")
        cmd.select("ca_atoms", "hb_residues and name CA")
        cmd.label("ca_atoms", "'%s-%s' % (resn, resi)")
        cmd.set("label_font_id", 18)
        cmd.set("cartoon_transparency", 0.3)
        cmd.select("focus_region", "ligand or hb_residues")
        cmd.zoom("ligand")
        cmd.orient("focus_region")
        cmd.center("focus_region")

        base_name = os.path.splitext(os.path.basename(pdb_file))[0]
        residues = []
        cmd.iterate("(hb_residues) and name CA", 
            "residues.append(f'{resn}-{resi}_{chain}')",
            space=locals())
        csv_path = os.path.join(output_dir, "Interacting_Residues.csv")
        write_interacting_residues_csv(csv_path, base_name, residues)

        interactions_output_image = os.path.join(output_dir, base_name + "_interaction.png")
        cmd.png(interactions_output_image, width=width, height=height, dpi=dpi, ray=1)
        interactions_session_file = os.path.join(output_dir, base_name + "_interaction.pse")
        cmd.save(interactions_session_file)
        
        return interactions_output_image, interactions_session_file
    
    finally:
        cmd.delete("all")

def surface_visualizations(pdb_file, output_dir, protein_color, ligand_color, residues_color,
                          width, height, dpi):
    if not separate_protein_ligand(pdb_file, output_dir):
        return None, None
    
    try:
        cmd.bg_color("white")
        cmd.set("surface_mode", 1)
        protein_selections = [name for name in cmd.get_names('selections') 
                            if name.startswith('protein_')]
        
        color_pool = cycle(COLOR_PRESETS[protein_color]["protein"])
        for chain_sel in protein_selections:
            cmd.color(next(color_pool), chain_sel)
            cmd.show("cartoon", chain_sel)
            cmd.set('cartoon_highlight_color', 'grey35')
            cmd.show("surface", chain_sel)
            cmd.set("transparency", 0.5)
            cmd.set("cartoon_transparency", 0)
        
        cmd.color(ligand_color, "ligand")
        cmd.set("transparency", 0, "ligand")
        cmd.show("surface", "ligand")
        cmd.hide("sticks", "ligand")

        cmd.select("proteins", " or ".join(protein_selections))
        cmd.select("hb_donors", "(proteins and donor) within 3.5 of (ligand and acceptor)")
        cmd.select("hb_acceptors", "(proteins and acceptor) within 3.5 of (ligand and donor)")
        cmd.select("hb_residues", "byres hb_donors or hb_acceptors")
        cmd.set("transparency", 0, "hb_residues")
        cmd.show("surface", "hb_residues")
        cmd.color(residues_color, "hb_residues")

        cmd.set('ray_trace_mode', 3)
        cmd.set('ray_trace_gain', 0.6)
        cmd.set('ambient', 0.3)
        cmd.set("direct", 0.6)
        cmd.set('specular', 0.2)
        cmd.set('shininess', 200)
        cmd.set('ray_shadow', 1)
        cmd.set('antialias', 4)
        #cmd.set("surface_quality", 4)

        cmd.select("focus_region", "ligand or hb_residues")
        cmd.orient("focus_region")
        cmd.zoom("all", 5)
        cmd.center("all")
        cmd.set("depth_cue", 0)
        
        base_name = os.path.splitext(os.path.basename(pdb_file))[0]
        output_overview_image = os.path.join(output_dir, base_name + "_complex_overview.png")
        cmd.png(output_overview_image, width=width, height=height, dpi=dpi, ray=1)
        surface_session_file = os.path.join(output_dir, base_name + "_complex_overview.pse")
        cmd.save(surface_session_file)
        
        return output_overview_image, surface_session_file
    
    finally:
        cmd.delete('all')