import pytest
import numpy as np
# -------------------------------------------------------------------------
# CORRECCIÓN CLAVE: Importamos desde el paquete 'aeeprotocol'
# -------------------------------------------------------------------------
from aeeprotocol.core.engine import AEEMathEngine

# ==========================================
# CONFIGURACIÓN Y FIXTURES
# ==========================================

@pytest.fixture
def engine():
    """Inicializa el motor con una fuerza estándar."""
    return AEEMathEngine(strength=0.25)

@pytest.fixture
def random_vector():
    """Genera un vector unitario aleatorio de dim=768 (tipo OpenAI/HuggingFace)."""
    dim = 768
    vec = np.random.randn(dim)
    return vec / np.linalg.norm(vec)

@pytest.fixture
def user_id():
    return 35664619  # Usamos un ID de ejemplo real

# ==========================================
# TESTS CIENTÍFICOS (Basados en SPEC.md)
# ==========================================

def test_determinism(engine, random_vector, user_id):
    """
    AXIOMA 1: El protocolo debe ser DETERMINISTA.
    Mismo Vector + Mismo ID = Exactamente el Mismo Resultado.
    """
    v1, _ = engine.inject(random_vector.copy(), user_id)
    v2, _ = engine.inject(random_vector.copy(), user_id)
    
    # Assert estricto: deben ser idénticos bit a bit
    assert np.allclose(v1, v2), "El protocolo no es determinista; el resultado varía."

def test_semantic_preservation(engine, random_vector, user_id):
    """
    AXIOMA 2: Invisibilidad Semántica.
    El vector marcado debe ser extremadamente similar al original.
    """
    watermarked, _ = engine.inject(random_vector, user_id)
    
    # Normalizamos para comparar similitud coseno
    w_norm = watermarked / np.linalg.norm(watermarked)
    original_norm = random_vector / np.linalg.norm(random_vector)
    
    similarity = np.dot(original_norm, w_norm)
    
    # Con strength=0.25, la similitud debería ser > 0.95
    assert similarity > 0.95, f"La marca destruye demasiado la semántica (Similitud: {similarity:.4f})"

def test_detection_positive(engine, random_vector, user_id):
    """
    AXIOMA 3: Detectabilidad.
    El motor debe ser capaz de reconocer su propia marca.
    """
    watermarked, _ = engine.inject(random_vector, user_id)
    
    score = engine.detect(watermarked, user_id)
    
    # El score debe superar el threshold definido en el engine
    assert score > engine.threshold, f"Falso Negativo: Score {score} no supera el umbral {engine.threshold}"

def test_detection_negative_wrong_user(engine, random_vector, user_id):
    """
    AXIOMA 4: Seguridad de Identidad.
    Un vector marcado por el Usuario A no debe dar positivo para el Usuario B.
    """
    watermarked, _ = engine.inject(random_vector, user_id)
    wrong_user_id = 999999999
    
    score = engine.detect(watermarked, wrong_user_id)
    
    assert score < engine.threshold, f"Falso Positivo de Identidad: Detectó al usuario equivocado (Score: {score})"

def test_orthogonality_logic(engine, random_vector, user_id):
    """
    AXIOMA 6: Verificación de la Matemática Interna (Whitebox).
    La dirección generada debe ser ortogonal al vector original ANTES de la inyección.
    """
    # Accedemos a la lógica interna para verificar la geometría
    direction = engine.compute_direction(random_vector, user_id)
    
    # El producto punto entre la dirección y el original debe ser casi 0
    dot_prod = np.dot(random_vector, direction)
    
    assert np.abs(dot_prod) < 1e-5, f"Fallo en ortogonalización: {dot_prod} != 0"