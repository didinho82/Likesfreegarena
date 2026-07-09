/**
 * @fileoverview Script para envio automático de 100 likes para Free Fire.
 * Integração com a API hospedada na Vercel.
 * @author Manus AI
 */

// Sua URL permanente da Vercel
const FREEFIRE_LIKE_API_BASE_URL = 'https://likesfreegarena-490bb536v-didosilva082-3763s-projects.vercel.app';

/**
 * Envia múltiplos likes para um UID específico.
 * @param {string} uid O ID do jogador.
 * @param {number} totalLikes Quantidade de likes desejada (padrão 100).
 */
async function sendMassiveFreeFireLikes(uid, totalLikes = 100) {
  if (!uid) {
    console.error('Erro: UID não fornecido.');
    return;
  }

  console.log(`Iniciando envio de ${totalLikes} likes para o UID: ${uid}...`);

  for (let i = 1; i <= totalLikes; i++) {
    try {
      const response = await fetch(`${FREEFIRE_LIKE_API_BASE_URL}/like?uid=${uid}`);
      const data = await response.json();

      if (response.ok) {
        console.log(`[${i}/${totalLikes}] Like enviado com sucesso!`);
      } else {
        console.warn(`[${i}/${totalLikes}] Aviso: ${data.message || 'Limite de contas atingido'}`);
        // Se a API avisar que não há mais contas disponíveis, paramos o loop
        if (data.message && data.message.includes("not found")) break;
      }
    } catch (error) {
      console.error(`[${i}/${totalLikes}] Erro na conexão:`, error.message);
    }
    
    // Pequena pausa de 100ms entre os envios para evitar bloqueios do navegador
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  console.log('Processo de envio finalizado.');
}

// Exemplo de como chamar no seu site:
// sendMassiveFreeFireLikes('SEU_UID_AQUI', 100);
