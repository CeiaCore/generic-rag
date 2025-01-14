
from src.project.default.domain.process.infra.repository.process import ProcessRepository
from src.project.default.domain.process.usecase.get_by_id_process import GetBydIdProcess, InputGetBydIdProcessDto


usecase = GetBydIdProcess(repository=ProcessRepository())

input = InputGetBydIdProcessDto(
    process_id="a2334ffe-2acf-4141-9a86-66ea8e142cd0"
)
print(usecase.execute(input).docs)