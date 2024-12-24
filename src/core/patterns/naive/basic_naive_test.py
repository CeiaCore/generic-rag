import pytest
from unittest.mock import Mock
from src.core.components.input.interface.InputInterface import InputInterface
from src.core.components.memory.interface.memory_interface import MemoryInterface
from src.core.components.retrieval.interface.retrieval_inteface import RetrievalInterface
from src.core.patterns.interface.pattern_interface import PatternInterface
from src.core.patterns.naive.basic_naive import BasicNaive, InputBasicNaiveDto



# Fixtures para os mocks das interfaces
@pytest.fixture
def input_component_mock():
    mock = Mock(spec=InputInterface)
    mock.input.return_value = "validated_query"
    return mock

@pytest.fixture
def retrieval_component_mock():
    mock = Mock(spec=RetrievalInterface)
    mock.retriever.return_value = ["document1", "document2"]
    return mock

@pytest.fixture
def memory_component_mock():
    mock = Mock(spec=MemoryInterface)
    mock.retrieve_memory.return_value = ["context1", "context2"]
    return mock

@pytest.fixture
def generator_component_mock():
    mock = Mock(spec=GeneratorInterface)
    mock.generate.return_value = "generated_response"
    return mock

@pytest.fixture
def basic_naive_instance(input_component_mock, retrieval_component_mock, memory_component_mock, generator_component_mock):
    return BasicNaive(
        input_component=input_component_mock,
        retrieval_component=retrieval_component_mock,
        memory_component=memory_component_mock,
        generator_component=generator_component_mock
    )

# Testes para InputBasicNaiveDto
def test_input_basic_naive_dto_initialization():
    dto = InputBasicNaiveDto(query="test_query", chat_id="123", file="file_path")
    assert dto.query == "test_query"
    assert dto.chat_id == "123"
    assert dto.file == "file_path"

# Testes para BasicNaive.execute
def test_basic_naive_execute_valid(basic_naive_instance, input_component_mock, retrieval_component_mock, memory_component_mock, generator_component_mock):
    input_dto = InputBasicNaiveDto(query="test_query", chat_id="123")

    result = basic_naive_instance.execute(input_dto)

    # Verifica chamadas e valores de retorno corretos
    input_component_mock.input.assert_called_once_with("test_query")
    retrieval_component_mock.retriever.assert_called_once_with("validated_query")
    memory_component_mock.save_memory.assert_called_once_with(chat_id="123", data=["document1", "document2"])
    memory_component_mock.retrieve_memory.assert_called_once_with("123")
    generator_component_mock.generate.assert_called_once_with(query="test_query", context=["context1", "context2"])

    assert result == "generated_response"


# Teste de caso onde não há documentos retornados pelo componente de recuperação
def test_basic_naive_execute_no_documents(basic_naive_instance, input_component_mock, retrieval_component_mock, memory_component_mock):
    input_dto = InputBasicNaiveDto(query="test_query", chat_id="123")
    retrieval_component_mock.retriever.return_value = []  # Nenhum documento

    result = basic_naive_instance.execute(input_dto)

    # Verificações de chamadas de método
    input_component_mock.input.assert_called_once_with("test_query")
    retrieval_component_mock.retriever.assert_called_once_with("validated_query")
    memory_component_mock.save_memory.assert_called_once_with(chat_id="123", data=[])
    memory_component_mock.retrieve_memory.assert_called_once_with("123")

    # Geração deve lidar com contexto vazio
    assert result == "generated_response"

# Teste de caso onde não há memória retornada
def test_basic_naive_execute_no_memory(basic_naive_instance, memory_component_mock, generator_component_mock):
    input_dto = InputBasicNaiveDto(query="test_query", chat_id="123")
    memory_component_mock.retrieve_memory.return_value = []  # Nenhuma memória

    result = basic_naive_instance.execute(input_dto)

    generator_component_mock.generate.assert_called_once_with(query="test_query", context=[])
    assert result == "generated_response"

# Teste de erro com componente de input falhando
def test_basic_naive_execute_input_failure(basic_naive_instance, input_component_mock):
    input_dto = InputBasicNaiveDto(query="test_query", chat_id="123")
    input_component_mock.input.side_effect = Exception("Input processing failed")

    with pytest.raises(Exception, match="Input processing failed"):
        basic_naive_instance.execute(input_dto)

# Teste de erro com falha no componente de recuperação
def test_basic_naive_execute_retrieval_failure(basic_naive_instance, retrieval_component_mock):
    input_dto = InputBasicNaiveDto(query="test_query", chat_id="123")
    retrieval_component_mock.retriever.side_effect = Exception("Retrieval failed")

    with pytest.raises(Exception, match="Retrieval failed"):
        basic_naive_instance.execute(input_dto)

# Teste de erro com falha no componente de geração
def test_basic_naive_execute_generator_failure(basic_naive_instance, generator_component_mock):
    input_dto = InputBasicNaiveDto(query="test_query", chat_id="123")
    generator_component_mock.generate.side_effect = Exception("Generation failed")

    with pytest.raises(Exception, match="Generation failed"):
        basic_naive_instance.execute(input_dto)
