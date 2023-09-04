import pandas as pd
from Bio import ExPASy, SwissProt


def get_swissprot_data(sprot_id):
    
    handle = ExPASy.get_sprot_raw(sprot_id)
    record = SwissProt.read(handle)
        
    results = pd.DataFrame({
            'ID' : sprot_id,
            'Entry_name' : record.entry_name,
            'Sequence' : record.sequence,
            'Sequence_length' : record.sequence_length,
    }, index=[0])
        
    return results
    

def caspase_cutter(sprot_id, caspase_set=None):
    
    if caspase_set is None:
        caspase_set = {
            "Caspase_1" : r"[FWYL].[HAT]D[^PEDQKR].{3}",
            "Caspase_2" : r"DVAD[^PEDQKR].{3}",
            "Caspase_3" : r"DMQD[^PEDQKR].{3}",
            "Caspase_4" : r"LEVD[^PEDQKR].{3}",
            "Caspase_5" : r"[LW]EHD.{4}",
            "Caspase_6" : r"VE[HI]D[^PEDQKR].{3}",
            "Caspase_7" : r"DEVD[^PEDQKR].{3}",
            "Caspase_8" : r"[IL]ETD[^PEDQKR].{3}",
            "Caspase_9" : r"LEHD.{4}",
            "Caspase_10" : r"IEAD.{4}"
            }
    
    results = pd.DataFrame(columns=['ID', 'Entry', 'Caspase', 'Site', 'Positions', 'Length'])
    i = 0
    
    for entry in sprot_id:
    
        data = get_swissprot_data(entry)
        
        for caspase, site in caspase_set.items():
            pattern = re.compile(site, re.IGNORECASE)
            
            for match in re.finditer(pattern, data.Sequence[0]):
                results.loc[i] = [ data.ID[0], data.Entry_name[0], caspase, match.group(), 
                            match.start()+4, data.Sequence_length[0] ]
                i += 1
    
    return results.drop_duplicates(ignore_index=True)
