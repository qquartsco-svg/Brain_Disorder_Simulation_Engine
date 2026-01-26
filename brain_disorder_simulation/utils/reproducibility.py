"""
재현성 보장 시스템

연구용 시뮬레이션을 위한 재현성 보장 모듈
- Seed 관리
- 실험 메타데이터
- 재현 가능한 랜덤 생성기
"""

import numpy as np
import hashlib
import json
import os
import platform
import subprocess
import uuid
from datetime import datetime
from typing import Dict, Optional, Any
from pathlib import Path


class ReproducibleRNG:
    """
    재현 가능한 랜덤 생성기
    
    모든 랜덤 연산은 여기서 관리되어 재현성을 보장합니다.
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        재현 가능한 RNG 초기화
        
        Args:
            seed: 시드 값 (None이면 자동 생성)
        """
        if seed is None:
            seed = np.random.randint(0, 2**32)
        
        self.seed = seed
        self.main_rng = np.random.default_rng(seed)
        
        # 서브시드 (엔진별 독립적 RNG)
        self.subseeds = {
            'attention': int(self.main_rng.integers(0, 2**32)),
            'impulse': int(self.main_rng.integers(0, 2**32)),
            'hyperactivity': int(self.main_rng.integers(0, 2**32)),
            'dopamine': int(self.main_rng.integers(0, 2**32)),
            'brain': int(self.main_rng.integers(0, 2**32))
        }
        
        # 서브 RNG 저장소
        self._sub_rngs = {}
    
    def get_rng(self, component: str = 'main') -> np.random.Generator:
        """
        컴포넌트별 RNG 반환
        
        Args:
            component: 컴포넌트 이름 ('main', 'attention', 'impulse', 등)
        
        Returns:
            RNG 인스턴스
        """
        if component == 'main':
            return self.main_rng
        
        if component not in self._sub_rngs:
            if component in self.subseeds:
                self._sub_rngs[component] = np.random.default_rng(self.subseeds[component])
            else:
                # 새로운 컴포넌트는 서브시드 생성
                subseed = int(self.main_rng.integers(0, 2**32))
                self.subseeds[component] = subseed
                self._sub_rngs[component] = np.random.default_rng(subseed)
        
        return self._sub_rngs[component]
    
    def reset(self, seed: Optional[int] = None):
        """RNG 리셋"""
        if seed is not None:
            self.seed = seed
        self.main_rng = np.random.default_rng(self.seed)
        self._sub_rngs = {}
        # 서브시드 재생성
        for key in self.subseeds:
            self.subseeds[key] = int(self.main_rng.integers(0, 2**32))


class ExperimentMetadata:
    """
    실험 메타데이터 관리
    
    재현성을 위한 필수 정보를 기록합니다.
    """
    
    def __init__(self, config: Dict[str, Any], seed: Optional[int] = None):
        """
        실험 메타데이터 초기화
        
        Args:
            config: 실험 설정 딕셔너리
            seed: 시드 값
        """
        self.experiment_id = str(uuid.uuid4())
        self.timestamp = datetime.now().isoformat()
        self.seed = seed if seed is not None else np.random.randint(0, 2**32)
        
        # 설정 해시 (재현성 검증용)
        config_str = json.dumps(config, sort_keys=True, default=str)
        self.config_hash = hashlib.sha256(config_str.encode()).hexdigest()
        
        # Git commit hash
        self.git_commit = self._get_git_commit()
        
        # 플랫폼 정보
        self.platform_info = {
            'os': platform.system(),
            'os_version': platform.version(),
            'python_version': platform.python_version(),
            'cpu_count': os.cpu_count() if hasattr(os, 'cpu_count') else None,
            'architecture': platform.machine()
        }
        
        # 결과 파일 경로 (나중에 설정)
        self.result_path = None
    
    def _get_git_commit(self) -> str:
        """Git commit hash 가져오기"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return 'unknown'
    
    def to_dict(self) -> Dict[str, Any]:
        """메타데이터를 딕셔너리로 변환"""
        return {
            'experiment_id': self.experiment_id,
            'timestamp': self.timestamp,
            'seed': self.seed,
            'config_hash': self.config_hash,
            'git_commit': self.git_commit,
            'platform_info': self.platform_info,
            'result_path': self.result_path
        }
    
    def save(self, filepath: str):
        """메타데이터를 JSON 파일로 저장"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'ExperimentMetadata':
        """저장된 메타데이터 로드"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # 임시 객체 생성 (config는 복원 불가능하므로 빈 딕셔너리)
        metadata = cls.__new__(cls)
        metadata.experiment_id = data['experiment_id']
        metadata.timestamp = data['timestamp']
        metadata.seed = data['seed']
        metadata.config_hash = data['config_hash']
        metadata.git_commit = data['git_commit']
        metadata.platform_info = data['platform_info']
        metadata.result_path = data.get('result_path')
        
        return metadata

