/**
 * @fileoverview Script JavaScript para integrar com a API de envio de likes do Free Fire.
 * Permite enviar likes para um UID específico de forma assíncrona.
 * @author Manus AI
 */

const FREEFIRE_LIKE_API_BASE_URL = 'https://5000-iqxl9di9p9beygfss5x2j-5963ee89.us2.manus.computer';

/**
 * Envia um like para um UID específico do Free Fire.
 * @param {string} uid O ID numérico do jogador (UID) para o qual o like será enviado.
 * @returns {Promise<object>} Uma promessa que resolve com a resposta da API ou rejeita com um erro.
 */
async function sendFreeFireLike(uid) {
  if (!uid) {
    throw new Error('O UID do jogador é obrigatório.');
  }

  const url = `${FREEFIRE_LIKE_API_BASE_URL}/like?uid=${uid}`;

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();

    if (!response.ok) {
      // Se a resposta não for OK (status 2xx), lança um erro com a mensagem da API
      throw new Error(data.message || data.error || 'Erro ao enviar like.');
    }

    return data;
  } catch (error) {
    console.error('Erro na requisição da API de likes:', error);
    throw error; // Rejeita a promessa para que o chamador possa lidar com o erro
  }
}

// Exemplo de uso (pode ser removido ou adaptado para seu site):
/*
(async () => {
  const playerUid = '1234567890'; // Substitua pelo UID real do jogador
  try {
    const result = await sendFreeFireLike(playerUid);
    console.log('Like enviado com sucesso:', result);
    // Atualize a interface do usuário com a mensagem de sucesso
  } catch (error) {
    console.error('Falha ao enviar like:', error.message);
    // Atualize a interface do usuário com a mensagem de erro
  }
})();
*/
