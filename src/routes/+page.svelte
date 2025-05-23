<script lang="ts">
  import { goto } from '$app/navigation';
  import { calculateDistance } from '../lib/api';
  let source = '';
  let destination = '';
  let unit: 'miles' | 'kilometers' | 'both' = 'miles';
  let loading = false;
  let error = '';
  let result: { miles?: number; kilometers?: number } | null = null;
  let showErrorToast = false;
  let errorToastTitle = 'Calculation failed';
  let errorToastMessage = 'Something went wrong and the calculation failed.';

  // Calculator SVG Icon as a string
  const calculatorIcon = `<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' fill='none' viewBox='0 0 24 24'><rect width='18' height='18' x='3' y='3' fill='#fff' stroke='#fff' stroke-width='2' rx='2'/><rect width='18' height='18' x='3' y='3' stroke='#B32D0F' stroke-width='2' rx='2'/><rect width='12' height='3' x='6' y='6' fill='#B32D0F'/><rect width='2' height='2' x='7' y='10' fill='#B32D0F'/><rect width='2' height='2' x='11' y='10' fill='#B32D0F'/><rect width='2' height='2' x='15' y='10' fill='#B32D0F'/><rect width='2' height='2' x='7' y='14' fill='#B32D0F'/><rect width='2' height='2' x='11' y='14' fill='#B32D0F'/><rect width='2' height='2' x='15' y='14' fill='#B32D0F'/></svg>`;

  const spinnerIcon = `<svg class='spinner' width='20' height='20' viewBox='0 0 50 50'><circle class='path' cx='25' cy='25' r='20' fill='none' stroke='#fff' stroke-width='5'></circle></svg>`;

  function viewHistory() {
    goto('/history');
  }

  // Clean address by removing 'Suite' and anything after, extra commas, and trimming whitespace
  function cleanAddress(address: string): string {
    let cleaned = address.replace(/suite.*$/i, '');
    cleaned = cleaned.replace(/,+/g, ',').replace(/\s+,/g, ',').replace(/,+\s*/g, ',').trim();
    cleaned = cleaned.replace(/,+$/, '').trim();
    return cleaned;
  }

  function isValidAddress(address: string): boolean {
    if (!address || address.trim().length < 5) return false;
    // All numbers
    if (/^\d+$/.test(address.trim())) return false;
    // No letters
    if (!/[a-zA-Z]/.test(address)) return false;
    // Only special characters
    if (/^[^a-zA-Z0-9]+$/.test(address.trim())) return false;
    return true;
  }

  async function calculate() {
    loading = true;
    error = '';
    result = null;
    showErrorToast = false;
    errorToastTitle = 'Calculation failed';
    errorToastMessage = 'Something went wrong and the calculation failed.';
    // Validation
    if (!source || !destination) {
      errorToastTitle = 'Missing address';
      errorToastMessage = 'Please enter both source and destination addresses.';
      showErrorToast = true;
      loading = false;
      return;
    }
    if (!isValidAddress(source)) {
      errorToastTitle = 'Invalid source address';
      errorToastMessage = 'Please enter a valid source address.';
      showErrorToast = true;
      loading = false;
      return;
    }
    if (!isValidAddress(destination)) {
      errorToastTitle = 'Invalid destination address';
      errorToastMessage = 'Please enter a valid destination address.';
      showErrorToast = true;
      loading = false;
      return;
    }
    if (source.trim().toLowerCase() === destination.trim().toLowerCase()) {
      errorToastTitle = 'Identical addresses';
      errorToastMessage = 'Source and destination addresses cannot be the same.';
      showErrorToast = true;
      loading = false;
      return;
    }
    try {
      const apiResult = await calculateDistance(source, destination);
      if (unit === 'miles') result = { miles: apiResult.miles };
      else if (unit === 'kilometers') result = { kilometers: apiResult.kilometers };
      else result = { miles: apiResult.miles, kilometers: apiResult.kilometers };
    } catch (e: any) {
      errorToastTitle = 'Calculation failed';
      errorToastMessage = e.message || 'Something went wrong and the calculation failed.';
      showErrorToast = true;
    } finally {
      loading = false;
    }
  }

  function closeToast() {
    showErrorToast = false;
  }
</script>

<!-- Error Toast Notification -->
{#if showErrorToast}
  <div class="error-toast">
    <div class="error-toast-icon">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="12" fill="#bf281c"/><path d="M8.47 8.47l7.06 7.06M15.53 8.47l-7.06 7.06" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>
    </div>
    <div class="error-toast-content">
      <div class="error-toast-title">{errorToastTitle}</div>
      <div class="error-toast-message">{errorToastMessage}</div>
    </div>
    <button class="error-toast-close" on:click={closeToast} aria-label="Close error notification">&times;</button>
  </div>
{/if}

<style>
  /* Keep input underline grey even when focused or filled */
  .container input[type="text"] {
    border-bottom: 2px solid #ccc !important;
    background: #fafaf8;
    transition: border-color 0.2s;
  }
  .container input[type="text"]:focus,
  .container input[type="text"]:active {
    outline: none;
    border-bottom: 2px solid #ccc !important;
    background: #fafaf8;
  }
  /* Override browser autofill blue/yellow background */
  .container input:-webkit-autofill,
  .container input:-webkit-autofill:focus,
  .container input:-webkit-autofill:active,
  .container input:-webkit-autofill:hover {
    -webkit-box-shadow: 0 0 0 1000px #fafaf8 inset !important;
    box-shadow: 0 0 0 1000px #fafaf8 inset !important;
    -webkit-text-fill-color: #222 !important;
    caret-color: #222;
  }
  .error-toast {
    position: fixed;
    right: 2.5rem;
    bottom: 2.5rem;
    background: #fff;
    border: 1.5px solid #bf281c;
    border-radius: 6px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1.1rem 1.5rem 1.1rem 1.1rem;
    min-width: 320px;
    z-index: 1000;
    animation: fadeIn 0.2s;
  }
  .error-toast-icon {
    flex-shrink: 0;
    margin-top: 0.1rem;
  }
  .error-toast-title {
    font-weight: 700;
    color: #bf281c;
    font-size: 1.08rem;
    margin-bottom: 0.1rem;
  }
  .error-toast-message {
    color: #313030;
    font-size: 0.98rem;
  }
  .error-toast-close {
    background: none;
    border: none;
    color: #bf281c;
    font-size: 1.5rem;
    font-weight: 700;
    margin-left: 1.2rem;
    margin-top: 0.1rem;
    cursor: pointer;
    line-height: 1;
    padding: 0 0.2rem;
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .spinner {
    animation: spin 1s linear infinite;
    vertical-align: middle;
  }
  @keyframes spin {
    100% { transform: rotate(360deg); }
  }
  .spinner .path {
    stroke-linecap: round;
  }
  .container {
    padding: 1rem 2rem 2rem 2rem;
    max-width: 1312px;
    width: 100%;
    min-height: 800px;
    margin: 0 auto;
    background: #f8f8f6;
    border-radius: 8px;
    box-sizing: border-box;
  }
  .top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }
  @media (max-width: 900px) {
    .container {
      padding: 0.5rem 0.5rem 1.5rem 0.5rem;
      min-height: 600px;
    }
    .top-bar {
      flex-direction: column;
      align-items: stretch;
      gap: 1rem;
    }
    .top-bar .view-history-btn {
      align-self: flex-end;
      width: auto;
      margin-left: 0;
      margin-top: 0.5rem;
    }
  }
  @media (max-width: 600px) {
    .container {
      padding: 0.2rem 0.1rem 1rem 0.1rem;
      min-height: 400px;
    }
    .top-bar {
      flex-direction: column;
      align-items: stretch;
      gap: 0.5rem;
    }
    .top-bar .view-history-btn {
      width: 100%;
      margin-left: 0;
      margin-top: 0.7rem;
      font-size: 1.05rem;
      padding: 0.9rem 0;
    }
  }

  /* Custom radio button styles for Unit selection */
  fieldset input[type="radio"] {
    accent-color: #bf281c;
  }

  /* For browsers that do not support accent-color, add fallback */
  fieldset input[type="radio"]:checked {
    /* Hide default */
    /* appearance: none; */
    /* outline: 2px solid #bf281c; */
    /* box-shadow: 0 0 0 2px #fff, 0 0 0 4px #bf281c; */
  }
</style>

<div class="container">
  <div class="top-bar">
    <div style="display: flex; flex-direction: column;">
      <h1 style="font-size: 2rem; font-weight: 500; margin-bottom: 0;">Distance Calculator</h1>
      <p style="margin: 0.25rem 0 0 0; color: #555;">Prototype web application for calculating the distance between addresses.</p>
    </div>
    <button class="view-history-btn" on:click={viewHistory} style="background: #313030; color: #fff; padding: 0.6rem 1.2rem; border: none; border-radius: 4px; font-size: 0.95rem; margin-left: 2rem;">View Historical Queries</button>
  </div>

  <!-- Form Row -->
  <form on:submit|preventDefault={calculate} style="background: #fff; border-radius: 6px; padding: 2rem 1.5rem; display: flex; gap: 1.5rem; align-items: flex-start; flex-wrap: wrap; box-shadow: 0 1px 4px rgba(0,0,0,0.03);">
    <!-- Source Address and Button Column -->
    <div style="display: flex; flex-direction: column; gap: 0.5rem; min-width: 240px; flex: 1;">
      <label for="source-address" style="font-size: 0.95rem; color: #888; font-weight: 500;">Source Address</label>
      <input id="source-address" type="text" bind:value={source} placeholder="Input address" style="width: 100%; padding: 0.7rem; border: none; border-bottom: 2px solid #ccc; background: #fafaf8; border-radius: 2px 2px 0 0; font-size: 1.05rem;" />
      <button type="submit" disabled={!source || !destination || loading} style="margin-top: 1.2rem; width: 240px; display: flex; align-items: center; gap: 0.7rem; padding: 0.9rem 1.2rem; background: #bf281c; color: #fff; border: none; border-radius: 2px; font-size: 1.1rem; font-weight: 500; cursor: {(!source || !destination || loading) ? 'not-allowed' : 'pointer'}; opacity: {(!source || !destination || loading) ? 0.7 : 1};">
        {#if loading}
          <span>{@html spinnerIcon}</span>
          Calculating...
        {:else}
          Calculate Distance
          <span>{@html calculatorIcon}</span>
        {/if}
      </button>
      {#if error}
        <div style="color: #b00; margin-top: 0.5rem;">{error}</div>
      {/if}
    </div>
    <!-- Destination Address -->
    <div style="display: flex; flex-direction: column; gap: 0.5rem; min-width: 240px; flex: 1;">
      <label for="destination-address" style="font-size: 0.95rem; color: #888; font-weight: 500;">Destination Address</label>
      <input id="destination-address" type="text" bind:value={destination} placeholder="Input address" style="width: 100%; padding: 0.7rem; border: none; border-bottom: 2px solid #ccc; background: #fafaf8; border-radius: 2px 2px 0 0; font-size: 1.05rem;" />
    </div>
    <!-- Unit and Distance Row -->
    <div style="display: flex; flex-direction: row; align-items: flex-start; gap: 2.5rem; min-width: 320px;">
      <!-- Unit -->
      <fieldset style="border: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.7rem; min-width: 120px;">
        <legend style="font-size: 0.95rem; color: #888; font-weight: 500; margin-bottom: 0.25rem;">Unit</legend>
        <label for="unit-miles" style="display: flex; align-items: center; gap: 0.5rem; font-size: 1.05rem;"><input id="unit-miles" type="radio" bind:group={unit} value="miles" /> Miles</label>
        <label for="unit-kilometers" style="display: flex; align-items: center; gap: 0.5rem; font-size: 1.05rem;"><input id="unit-kilometers" type="radio" bind:group={unit} value="kilometers" /> Kilometers</label>
        <label for="unit-both" style="display: flex; align-items: center; gap: 0.5rem; font-size: 1.05rem;"><input id="unit-both" type="radio" bind:group={unit} value="both" /> Both</label>
      </fieldset>
      <!-- Distance Result -->
      <div style="min-width: 140px; font-size: 1.15rem; font-weight: 600; color: #222;">
        <label for="distance-value" style="font-size: 0.95rem; color: #888; font-weight: 500;">Distance</label><br>
        {#if result}
          <span id="distance-value">
            {#if result.miles !== undefined && result.kilometers !== undefined}
              {result.miles.toFixed(2)} mi / {result.kilometers.toFixed(2)} km
            {:else if result.miles !== undefined}
              {result.miles.toFixed(2)} mi
            {:else if result.kilometers !== undefined}
              {result.kilometers.toFixed(2)} km
            {/if}
          </span>
        {/if}
      </div>
    </div>
  </form>
</div>

