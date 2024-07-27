from flask import Flask, request, render_template, jsonify, send_file
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('CacheSim.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    block_size = int(request.form['blockSize'])
    set_size = int(request.form['setSize'])
    mm_size = request.form['mmSize']
    cache_size = request.form['cacheSize']
    program_flow = request.form['programFlow']

    # Convert mm_size and cache_size to blocks if necessary
    mm_size = int(mm_size.split()[0])
    cache_size = int(cache_size.split()[0])
    
    # Convert program_flow to a list of addresses
    program_flow = list(map(int, program_flow.split()))

    # Run the cache simulation
    results = cache_simulator(block_size, set_size, mm_size, cache_size, program_flow)

    return jsonify(results)

@app.route('/save_results', methods=['POST'])
def save_results():
    results = request.json
    output = io.StringIO()
    output.write("Cache Simulator Results\n")
    output.write(f"Cache Hits: {results['cacheHits']}\n")
    output.write(f"Cache Misses: {results['cacheMisses']}\n")
    output.write(f"Miss Penalty: {results['missPenalty']}\n")
    output.write(f"Average Memory Access Time: {results['avgMemoryAccessTime']}\n")
    output.write(f"Total Memory Access Time: {results['totalMemoryAccessTime']}\n")
    output.write("\nCache Snapshot:\n")
    output.write("Set | " + " | ".join(f"Block {i + 1}" for i in range(len(results['cacheSnapshot'][0]))) + "\n")
    output.write("-" * (len(results['cacheSnapshot'][0]) * 10 + 4) + "\n")
    for i, cache_set in enumerate(results['cacheSnapshot']):
        output.write(f"{i} | " + " | ".join(str(block) if block is not None else 'Empty' for block in cache_set) + "\n")
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/plain',
        download_name='cache_simulation_results.txt'
    )

def cache_simulator(block_size, set_size, mm_size, cache_size, program_flow):
    # Calculate the number of sets in the cache
    num_sets = cache_size // set_size
    
    # Initialize the cache and LRU tracking
    cache = [[None] * set_size for _ in range(num_sets)]
    lru = [[-1] * set_size for _ in range(num_sets)]
    
    hit_count = 0
    miss_count = 0
    time = 0
    miss_penalty = 10  # Assuming a fixed miss penalty
    total_memory_access_time = 0

    for address in program_flow:
        block = address // block_size
        set_index = block % num_sets
        
        if block in cache[set_index]:
            # Cache hit
            hit_count += 1
            lru[set_index][cache[set_index].index(block)] = time
        else:
            # Cache miss
            miss_count += 1
            if None in cache[set_index]:
                # There is an empty slot in the set
                empty_index = cache[set_index].index(None)
                cache[set_index][empty_index] = block
                lru[set_index][empty_index] = time
            else:
                # Evict the least recently used block
                lru_index = lru[set_index].index(min(lru[set_index]))
                cache[set_index][lru_index] = block
                lru[set_index][lru_index] = time
            total_memory_access_time += miss_penalty
        
        time += 1

    total_memory_access_time += len(program_flow)  # Add hit time (assuming 1 time unit per access)
    avg_memory_access_time = total_memory_access_time / len(program_flow)

    return {
        'cacheHits': hit_count,
        'cacheMisses': miss_count,
        'missPenalty': miss_penalty,
        'avgMemoryAccessTime': avg_memory_access_time,
        'totalMemoryAccessTime': total_memory_access_time,
        'cacheSnapshot': cache
    }

if __name__ == '__main__':
    app.run(debug=True)
