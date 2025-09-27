import concurrent.futures
import json

def process_chunk(chunk_lines, chunk_id):
    """
    Traite un chunk spécifique et extrait les exons.
    """
    chunks = {f"Chunk {chunk_id}": {"target": [], "query": []}}
    current_chunk = f"Chunk {chunk_id}"

    for line in chunk_lines:
        line = line.strip()
        if line.startswith("target"):
            sequence = line.split()[2]  # Extrait la partie de la séquence
            exon = sequence.replace("-", "")  # Retire les gaps '-'
            chunks[current_chunk]["target"].append(exon)

        elif line.startswith("query"):
            sequence = line.split()[2]
            exon = sequence.replace("-", "")
            chunks[current_chunk]["query"].append(exon)
    return chunks

def extract_exons_parallel(file_path, output_file, num_workers=24):
    """
    Lit un fichier très volumineux, divise en chunks et extrait les exons en parallèle.
    Stocke les résultats dans un fichier JSON.
    """
    chunk_size = 1000000  # Nombre de lignes par chunk
    results = []

    with open(file_path, "r") as file:
        # Diviser le fichier en chunks
        lines_buffer = []
        chunk_id = 0
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = []

            for line in file:
                lines_buffer.append(line)
                if len(lines_buffer) >= chunk_size:
                    # Soumettre un chunk pour traitement
                    futures.append(executor.submit(process_chunk, lines_buffer, chunk_id))
                    lines_buffer = []
                    chunk_id += 1

            # Soumettre les dernières lignes restantes
            if lines_buffer:
                futures.append(executor.submit(process_chunk, lines_buffer, chunk_id))

            # Récupérer les résultats
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

    # Sauvegarder les résultats dans un fichier JSON
    with open(output_file, "w") as outfile:
        json.dump(results, outfile, indent=4)

    print(f"Les résultats ont été sauvegardés dans {output_file}")

# Exécution
if __name__ == "__main__":
    file_path = "alignment_results.txt"  # Remplace par le chemin vers ton fichier
    output_file = "exons_resultats.json"  # Fichier pour sauvegarder les résultats
    num_workers = 24  # Nombre de cœurs disponibles

    extract_exons_parallel(file_path, output_file, num_workers)
