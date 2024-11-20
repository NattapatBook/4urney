import { ref, computed } from 'vue';

export function createWebSocket(path) {
  // path without starting and ending slash
  const protocol = 'ws' + window.location.protocol.substring(4); // ":" or "s:"
  return new WebSocket(`${protocol}//${window.location.host}/ws/${path}/`);
}

export function createPersistentWebSocket(path, handler) {
  const websocket = ref(null); // Store the WebSocket in a ref

  const ready = computed(() => !!websocket.value); // Computed property for websocket readiness

  const send = (data) => {
    if (websocket.value) {
      websocket.value.send(JSON.stringify(data));
    }
  };

  const close = () => {
    if (websocket.value) {
      websocket.value.close();
    }
  };

  function _createPersistentWebSocket() {
    websocket.value = null;
    const ws = createWebSocket(path);

    ws.onopen = () => {
      websocket.value = ws;
    };

    ws.onmessage = handler;

    ws.onclose = (e) => {
      console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
      setTimeout(() => {
        _createPersistentWebSocket();
      }, 1000);
    };

    ws.onerror = (err) => {
      console.error('Socket encountered error: ', err.message, 'Closing socket');
      ws.close();
    };
  }

  _createPersistentWebSocket();

  return {
    websocket, // Reactive reference to the WebSocket
    ready, // Computed property indicating WebSocket readiness
    send,
    close
  };
}
