A ideia desse projeto surgiu de um estalo: eu já tinha feito um gerador de QR Code usando bibliotecas prontas (qrcode e Pillow), e funcionava lindamente. Mas aí eu parei pra pensar: e se o criador dessa biblioteca decidir desativar o projeto amanhã? Eu ia ficar congelado sem saber o que fazer?

Eu não quero ser só mais um que "monta peças" dos outros. Eu quero ser programador de verdade, entender a base pra não ficar estagnado como um eterno júnior que só sabe repetir palavras mágicas. Então, decidi reconstruir tudo do zero.

O Desafio (ou: "Meu Deus, que complexo!")
Vou ser sincero: fazer um QR Code na mão é um soco no estômago. O buraco é muito mais embaixo do que eu imaginava:

Bits e Hexadecimal: Primeiro, você tem que converter tudo, limpar o código e lidar com um limite chatíssimo de bits.

Matemática de Galois (GF): Aqui a coisa ficou séria. Eu usei o Gemini para me ajudar a entender a base dessa matemática, porque é um nível de abstração absurdo. A IA me ajudou nos cálculos e na teoria, mas cada linha de código foi batida por mim.

Correção de Erros (Reed-Solomon): É bizarro pensar que você precisa criar "números extras" que servem como tolerância a falhas. Se você riscar o QR Code, ele ainda lê por causa dessa lógica de polinômios em um campo finito.

Por que BMP e não PNG?
Como o meu desafio era zero bibliotecas externas, eu não podia usar o Pillow (PIL) para salvar a imagem. Chegou um ponto que minha cabeça já estava fritando com tanta matemática que eu não ia conseguir codar um compressor de PNG do zero agora.

A solução? Fui de Bitmap (BMP). É muito mais "raiz". Você basicamente calcula onde cada pixel vai estar, gera o arquivo bruto e o computador entende. É a lógica pura, sem firula.

O que eu aprendi:
Esse projeto me provou que eu consigo ler documentação pesada e resolver problemas reais sem muletas. Se a biblioteca sumir, eu sei como o dado vira código e como o código vira imagem.
