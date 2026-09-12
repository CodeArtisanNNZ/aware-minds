<?php
// Server-side example only. Set AWARE_MINDS_KEY in your PHP server environment.
// Authenticate your own patient before invoking this endpoint.
$secret = getenv('AWARE_MINDS_KEY');
if (!$secret) { http_response_code(503); exit('AI integration not configured'); }
$question = trim((string) ($_POST['question'] ?? ''));
if ($question === '' || strlen($question) > 12000) { http_response_code(400); exit('Invalid question'); }
$body = json_encode(['app_id' => 'healthcare-central', 'message' => $question], JSON_THROW_ON_ERROR);
$handle = curl_init(rtrim(getenv('AWARE_MINDS_URL') ?: 'http://127.0.0.1:8000', '/') . '/api/v1/integrations/healthcare-central/chat');
curl_setopt_array($handle, [CURLOPT_POST => true, CURLOPT_POSTFIELDS => $body, CURLOPT_HTTPHEADER => ['Authorization: Bearer ' . $secret, 'Content-Type: application/json'], CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 120]);
$result = curl_exec($handle);
http_response_code(curl_getinfo($handle, CURLINFO_HTTP_CODE) ?: 502);
header('Content-Type: application/json');
echo $result === false ? json_encode(['error' => 'AI service unavailable']) : $result;
curl_close($handle);
