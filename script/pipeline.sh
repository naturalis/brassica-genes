bash script_shortlist.sh
python3 slice_script.py
bash blast.sh
python3 blast_selector.py
python3 slice_script.py
python3 translator.py
bash alignments.sh
python3 variant_caller.py
bash total_variance.sh
python3 tsv_creator.py

