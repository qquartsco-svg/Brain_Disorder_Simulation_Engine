# Alpha vNext - Evaluation Layer (Objective Functions) v1.0

본 문서는 **Brain Disorder Simulation Engine(연구/의료용 baseline)** 위에 얹는 **Alpha vNext(Self-Regulating Meta-Brain)**의 **Layer 2(평가층)**을 고정한다.

- 목표: Layer 3(SelfRegulationController)가 **모드 전환/액션 선택**을 할 수 있도록, 관측치로부터 **닫힌 수식 형태의 목표함수/지표**를 제공한다.
- 주의: 연구/교육용. 의학적 진단/치료 권고 아님.

---

## 0) 공통 정의

### 0.1 Observation vector
시간 t의 관측치(plant에서 추출):

- 상태: \(E_t\)(energy), \(A_t\)(arousal), \(Att_t\)(attention), \(Imp_t\)(impulsivity)
- 루프 강도: \(s_i(t)\in[0,1]\) (negative_bias, hyperarousal, intrusive_memory, avoidance, energy_collapse, motivation_collapse, attention_instability, rpe, ...)
- (선택) 변화율: \(\Delta E_t, \Delta A_t, \Delta Att_t\)

### 0.2 Normalization
- \(\mathrm{clip}(x)=\min(1,\max(0,x))\)
- 모든 점수는 **좋을수록 1**로 통일한다.

---

## 1) Inference 4축 (0~1)

### 1.1 Homeostasis score \(H_t\)

\[
H_t=\mathrm{clip}(\alpha_E H_E+\alpha_A H_A+\alpha_L H_L)\quad\text{with}\quad \alpha_E+\alpha_A+\alpha_L=1
\]

- 에너지 안정:
\[
H_E=\mathrm{clip}\Big(1-\frac{|E_t-E^\*|}{E_{tol}}\Big)
\]
- 각성 안정:
\[
H_A=\mathrm{clip}\Big(1-\frac{|A_t-A^\*|}{A_{tol}}\Big)
\]
- 루프 과열 페널티(정규화 고정):
\[
H_L=\mathrm{clip}\Big(1-\frac{\sum_i w_i s_i(t)}{\sum_i w_i}\Big)
\]

> **고정 규칙 A-2**: \(L_{max}\)는 \(\sum_i w_i\)로 고정하여 \(H_L\) 정규화를 닫는다.

### 1.2 Signal-to-Noise score \(S_t\)

\[
S_t=\mathrm{clip}(\beta_{att}Att_t+\beta_{imp}(1-Imp_t)+\beta_{rpe}(1-s_{rpe}(t)))\quad\text{with}\quad\beta_{att}+\beta_{imp}+\beta_{rpe}=1
\]

### 1.3 Flexibility score \(F_t\)

고착 루프 집합 \(\mathcal{K}\) (예: intrusive_memory, avoidance, negative_bias, hyperarousal, control_failure):

\[
F_t=\mathrm{clip}\Big(1-\sum_{k\in\mathcal{K}}\gamma_k s_k(t)\Big)\quad\text{with}\quad \sum_{k\in\mathcal{K}}\gamma_k=1
\]

### 1.4 Motivation score \(M_t\)

\[
M_t=\mathrm{clip}\Big(1-\delta_{mc}s_{motivation\_collapse}(t)-\delta_{ec}s_{energy\_collapse}(t)\Big)\quad\text{with}\quad \delta_{mc}+\delta_{ec}=1
\]

> **고정 규칙 A-1**: 각 축 조합 가중치는 합이 1이 되도록 강제한다.

---

## 2) Stress index \(X_t\) (0~1)

\[
X_t=\mathrm{clip}\Big(\sum_i \eta_i s_i(t)+\eta_{\Delta}\,\mathrm{clip}(|\Delta E_t|+|\Delta A_t|+|\Delta Att_t|)\Big)
\]

MVP에서는 변화율 항(\(\eta_{\Delta}\))을 0으로 두고 시작 가능.

---

## 3) Performance index \(P_t\)

\[
P_t=\mathrm{clip}\Big(\frac{H_t+S_t+F_t+M_t}{4}\Big)
\]

---

## 4) Emergence score \(Emerge_t\) (창발/보상 근사)

- 목적: **stress가 있는데도 성능이 유지/상승되는 구간**을 창발 이벤트로 포착
- 원칙: **stress=0이면 창발로 치지 않음**

\[
Emerge_t=\mathrm{clip}\Big(\frac{P_t-\lambda X_t-\tau}{1-\tau}\Big)\cdot \mathbb{1}[X_t\ge X_{min}]
\]

> **고정 규칙 A-3**: 위 식의 괄호/정규화 형태를 그대로 고정한다.

해석:
- \(X_t\ge X_{min}\): 충분한 stress 구간에서만 창발을 기록
- \(P_t-\lambda X_t>\tau\): stress 대비 성능이 baseline을 넘는 구간만 창발로 인정

---

## 5) Layer 3(제어층) 연동 규약(평가층 관점)

- 평가층은 **"좋다/나쁘다" 진단**이 아니라, 제어층이 사용할 **피드백 신호**를 제공한다.
- Explore는 **stress를 올리되**, \(P_t\)를 유지하며 \(Emerge_t\) 이벤트를 얻는 모드다.
- Stabilize는 \(H_t\uparrow, X_t\downarrow\)를 우선하는 모드다.

---

## 6) 필수 가드레일(요약)

Layer 3는 반드시 다음 안전 불변식을 가진다.

- Energy floor: \(E_t\ge E_{min}\)
- Loop saturation cap: \(s_i(t)\le s_{max}\) (예: 0.9)
- Explore duration limit: 연속 N step 제한
- Recovery deadline: Explore 종료 후 M step 내 \(H_t\ge H_{safe}\) 복귀 실패 시 Reset

