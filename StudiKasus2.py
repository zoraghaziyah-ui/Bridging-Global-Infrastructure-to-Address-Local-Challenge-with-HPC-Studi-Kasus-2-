import time
import numpy as np
import pandas as pd
from multiprocessing import Pool, cpu_count

def simulate_evacuation_agent(agent_id):
    """
    Fungsi untuk mensimulasikan perhitungan rute evakuasi 
    dan penghitungan risiko bagi satu agen/kendaraan.
    """
    np.random.seed(agent_id)
   
    start_pos = np.random.uniform(0, 100, size=2)
    safe_zone = np.array([100.0, 100.0])

    simulated_steps = 1000
    current_pos = start_pos.copy()
    total_time = 0.0
    
    for _ in range(simulated_steps):
        distance_vector = safe_zone - current_pos
        risk_factor = np.sin(current_pos[0]) * np.cos(current_pos[1]) + 1.5
        speed = np.random.uniform(20, 60) / risk_factor

        step_move = (distance_vector / np.linalg.norm(distance_vector)) * (speed / 3600.0)
        current_pos += step_move
        total_time += 1.0 / speed
        
        if np.linalg.norm(safe_zone - current_pos) < 1.0:
            break

    return {
        'Agent_ID': agent_id,
        'Initial_Distance_KM': round(float(np.linalg.norm(safe_zone - start_pos)), 2),
        'Evacuation_Time_Hours': round(float(total_time), 4),
        'Status': 'Evacuated'
    }

if __name__ == '__main__':
    print("=== SIMULASI EVAKUASI BENCANA DENGAN KOMPUTASI PARALEL (HPC-STYLE) ===")

    NUM_AGENTS = 50000
    num_cores = cpu_count()
    
    print(f"Jumlah Agen Evakuasi : {NUM_AGENTS}")
    print(f"Jumlah Core CPU Aktif: {num_cores} cores")
    print("\nMemulai perhitungan komputasi paralel...")
    
    start_time = time.time()
    
    with Pool(processes=num_cores) as pool:
        results = pool.map(simulate_evacuation_agent, range(NUM_AGENTS))
        
    execution_time = time.time() - start_time
    
    df_results = pd.DataFrame(results)
    
    print("\n=== HASIL EKSEKUSI SIMULASI ===")
    print(f"Total Waktu Komputasi : {execution_time:.2f} detik")
    print(f"Kecepatan Pemrosesan  : {NUM_AGENTS / execution_time:.2f} agen/detik")
    print("\n5 Sampel Hasil Simulasi Evakuasi:")
    print(df_results.head())

    df_results.to_csv("evacuation_simulation_results.csv", index=False)
    print("\nHasil simulasi berhasil disimpan ke 'evacuation_simulation_results.csv'")