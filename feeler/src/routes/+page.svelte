<script>
    import { onMount } from 'svelte';
    let text = '';
    let emotions = [];
  
    const analyzeText = async (inputText) => {
      if (inputText) {
        const response = await fetch('http://localhost:5000/analyze', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text: inputText })
        });
  
        if (response.ok) {
          const data = await response.json();
          emotions = data.emotions;
        } else {
          console.error('Failed to fetch data');
        }
      }
    };
  
    $: if (text) {
      analyzeText(text);
    }
  </script>
  
  <style>
    .emotion {
      display: flex;
      align-items: center;
      margin-top: 10px;
    }
    .emotion img {
      width: 24px;
      height: 24px;
      margin-left: 10px;
    }
    .emotion-container {
      margin-top: 20px;
    }
    .input-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-top: 20px;
    }
    .input-box {
      resize: none;
      outline: none;
      background-color: rgb(170, 148, 197);
      height: 100px;
      width: 400px;
      font-size: 18px;
      padding: 10px;
    }
  </style>
  
  <main>
    <h1>Analisis Emosi</h1>
    <div class="input-container">
      <input type="text" bind:value={text} class="input-box" placeholder="Ketik pesan Anda di sini..."/>
      <div class="emotion-container">
        {#each emotions as {word, emotion, image}}
          <div class="emotion">
            <p>{word} - {emotion}</p>
            <img src={image} alt={emotion} />
          </div>
        {/each}
      </div>
    </div>
  </main>
  