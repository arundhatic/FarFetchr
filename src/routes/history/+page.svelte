<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { getHistory } from '../../lib/api';
  type Query = {
    source: string;
    destination: string;
    unit: string;
    result: { miles?: number; kilometers?: number };
    timestamp: string;
  };
  let history: Query[] = [];
  let loading = true;
  let error = '';
  let page = 1;
  const pageSize = 10;
  let pageCount = 0;
  let paginated: Query[] = [];
  let addressFilter = '';
  let filterType: 'both' | 'source' | 'destination' = 'both';
  let minDistance: number | '' = '';
  let maxDistance: number | '' = '';

  onMount(async () => {
    loading = true;
    error = '';
    try {
      const data = await getHistory();
      // The backend returns { history: [ ... ] }
      history = data.history.map(q => ({
        source: q.source,
        destination: q.destination,
        result: { miles: q.miles, kilometers: q.kilometers },
        timestamp: q.timestamp
      }));
      pageCount = Math.ceil(history.length / pageSize);
      paginated = history.slice((page - 1) * pageSize, page * pageSize);
    } catch (e: any) {
      error = e.message || 'Failed to load history';
    } finally {
      loading = false;
    }
  });

  function backToCalculator() {
    goto('/');
  }

  function clearFilters() {
    addressFilter = '';
    filterType = 'both';
    minDistance = '';
    maxDistance = '';
  }

  $: filtered = history.filter(q => {
    // Address filter
    const addressMatch =
      !addressFilter ||
      (filterType === 'source'
        ? q.source.toLowerCase().includes(addressFilter.toLowerCase())
        : filterType === 'destination'
        ? q.destination.toLowerCase().includes(addressFilter.toLowerCase())
        : q.source.toLowerCase().includes(addressFilter.toLowerCase()) ||
          q.destination.toLowerCase().includes(addressFilter.toLowerCase()));

    // Distance filter (miles)
    const miles = q.result.miles ?? 0;
    const distanceMatch =
      (!minDistance || miles >= Number(minDistance)) &&
      (!maxDistance || miles <= Number(maxDistance));

    return addressMatch && distanceMatch;
  });

  $: pageCount = Math.ceil(filtered.length / pageSize);
  $: paginated = filtered.slice((page - 1) * pageSize, page * pageSize);

  // Add a white calculator SVG icon for the back button
  const calculatorIcon = `<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' fill='none' viewBox='0 0 24 24'><rect width='18' height='18' x='3' y='3' fill='none' stroke='#313030' stroke-width='2' rx='2'/><rect width='12' height='3' x='6' y='6' fill='#313030'/><rect width='2' height='2' x='7' y='10' fill='#313030'/><rect width='2' height='2' x='11' y='10' fill='#313030'/><rect width='2' height='2' x='15' y='10' fill='#313030'/><rect width='2' height='2' x='7' y='14' fill='#313030'/><rect width='2' height='2' x='11' y='14' fill='#313030'/><rect width='2' height='2' x='15' y='14' fill='#313030'/></svg>`;
</script>

<div class="container-history">
  <!-- Top Bar -->
  <div class="history-top-bar">
    <div class="history-title-group">
      <h1>Distance Calculator</h1>
      <p>Prototype web application for calculating the distance between addresses.</p>
    </div>
    <button
      class="back-btn"
      on:click={backToCalculator}
      aria-label="Back to Calculator"
      style="display: flex; align-items: center; gap: 0.7rem; background: #ededed; color: #313030; min-width: 220px; height: 48px; padding: 0.6rem 1.2rem; border: 1.2px solid #313030; border-radius: 0; font-size: 0.95rem; font-weight: 400; margin: 0; box-shadow: none; justify-content: center;"
    >
      Back to Calculator
      <span>{@html calculatorIcon}</span>
    </button>
  </div>

  <div class="history-box">
    <div class="history-header">
      <div class="history-header-title">Historical Queries</div>
      <div class="history-header-desc">History of the user's queries.</div>
      <div style="display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 0.5rem; align-items: flex-end; margin-bottom: 1.2rem;">
        <div>
          <label style="font-size:0.95rem; color:#888;">Address</label><br />
          <input
            type="text"
            placeholder="Filter by address..."
            bind:value={addressFilter}
            style="padding: 0.5rem 1rem; border: 1px solid #ccc; border-radius: 4px; font-size: 1rem; width: 180px;"
            aria-label="Filter address"
          />
          <select bind:value={filterType} style="margin-left:0.5rem; padding:0.5rem; font-size:1rem;">
            <option value="both">Source or Destination</option>
            <option value="source">Source Only</option>
            <option value="destination">Destination Only</option>
          </select>
        </div>
        <div>
          <label style="font-size:0.95rem; color:#888;">Distance (mi)</label><br />
          <input type="number" min="0" placeholder="Min" bind:value={minDistance} style="width:70px; padding:0.5rem; border:1px solid #ccc; border-radius:4px; font-size:1rem;" aria-label="Min distance" />
          <span style="margin:0 0.3rem;">-</span>
          <input type="number" min="0" placeholder="Max" bind:value={maxDistance} style="width:70px; padding:0.5rem; border:1px solid #ccc; border-radius:4px; font-size:1rem;" aria-label="Max distance" />
        </div>
        <button type="button" on:click={clearFilters} style="margin-left:1rem; padding:0.6rem 1.2rem; font-size:1rem; background:#ededed; color:#313030; border:1px solid #ccc; border-radius:0; cursor:pointer;">Clear Filters</button>
      </div>
    </div>
    <div class="history-table-wrap">
      <table class="history-table">
        <thead>
          <tr>
            <th>Source Address</th>
            <th>Destination Address</th>
            <th>Distance in Miles</th>
            <th>Distance in Kilometers</th>
          </tr>
        </thead>
        <tbody>
          {#if history.length === 0}
            <tr><td colspan="4" style="text-align:center; color:#888;">No historical queries found.</td></tr>
          {:else}
            {#each paginated as q}
              <tr>
                <td>{q.source}</td>
                <td>{q.destination}</td>
                <td>{q.result.miles !== undefined ? q.result.miles.toFixed(2) + ' mi' : '-'}</td>
                <td>{q.result.kilometers !== undefined ? q.result.kilometers.toFixed(2) + ' km' : '-'}</td>
              </tr>
            {/each}
          {/if}
        </tbody>
      </table>
    </div>
    <div class="pagination" style="margin-top: 1rem; display: flex; align-items: center; gap: 1rem;">
      <button on:click={() => page = Math.max(1, page - 1)} disabled={page === 1}>Previous</button>
      <span>Page {page} of {pageCount}</span>
      <button on:click={() => page = Math.min(pageCount, page + 1)} disabled={page === pageCount}>Next</button>
    </div>
  </div>
</div>

<style>
  .container-history {
    padding: 1rem 2rem 2rem 2rem;
    max-width: 1312px;
    width: 100%;
    min-height: 800px;
    margin: 0 auto;
    background: #f8f8f6;
    border-radius: 8px;
    box-sizing: border-box;
  }
  @media (max-width: 900px) {
    .container-history {
      padding: 0.5rem 0.5rem 1.5rem 0.5rem;
      min-height: 600px;
    }
    .history-top-bar, .history-title-group {
      flex-direction: column !important;
      align-items: flex-start !important;
      gap: 1rem !important;
    }
    .history-box {
      padding: 1.2rem 0.5rem 1.5rem 0.5rem;
    }
    .history-table th, .history-table td {
      font-size: 0.95rem;
      padding: 0.5rem 0.4rem;
    }
  }
  @media (max-width: 600px) {
    .container-history {
      padding: 0.2rem 0.1rem 1rem 0.1rem;
      min-height: 400px;
    }
    .history-top-bar, .history-title-group {
      flex-direction: column !important;
      align-items: flex-start !important;
      gap: 0.5rem !important;
    }
    .history-box {
      padding: 0.7rem 0.1rem 1rem 0.1rem;
    }
    .history-table th, .history-table td {
      font-size: 0.9rem;
      padding: 0.3rem 0.2rem;
    }
  }
  .history-top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }
  .history-title-group h1 {
    font-size: 2rem;
    font-weight: 500;
    margin-bottom: 0;
  }
  .history-title-group p {
    margin: 0.25rem 0 0 0;
    color: #555;
  }
  .back-btn {
    background: #313030;
    color: #fff;
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 0;
    font-size: 0.95rem;
    margin-left: 2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    font-weight: 500;
  }
  .back-icon {
    font-size: 1.1rem;
    margin-right: 0.3rem;
    display: inline-block;
    transform: translateY(-1px);
  }
  .history-box {
    background: #fff;
    border-radius: 8px;
    padding: 1.5rem 1.5rem 2rem 1.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03);
  }
  .history-header-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.1rem;
  }
  .history-header-desc {
    color: #888;
    font-size: 0.98rem;
    margin-bottom: 1.2rem;
  }
  .history-table-wrap {
    overflow-x: auto;
  }
  .history-table {
    width: 100%;
    border-collapse: collapse;
    background: #fff;
  }
  .history-table th {
    background: #ededed;
    color: #313030;
    font-weight: 600;
    font-size: 1rem;
    padding: 0.7rem 0.8rem;
    text-align: left;
    border-bottom: 2px solid #e0e0e0;
  }
  .history-table td {
    font-size: 1rem;
    color: #313030;
    padding: 0.7rem 0.8rem;
    border-bottom: 1px solid #f0f0f0;
    background: #fafaf8;
  }
  .history-table tr:last-child td {
    border-bottom: none;
  }
  .pagination button {
    background: #313030;
    color: #fff;
    border: none;
    border-radius: 0;
    padding: 0.4rem 1.1rem;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    opacity: 1;
    transition: opacity 0.2s;
  }
  .pagination button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  button[type="button"] {
    border-radius: 0 !important;
  }
</style> 