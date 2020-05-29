class Units():
    # Unit converts between common units

    # ECU measures flow in [0.1SLM]
    @staticmethod
    def ecu_to_slm(flow: int) -> float:
        return float(flow) * 0.01

    @staticmethod
    def slm_to_ecu(flow: float) -> int:
        return int(flow * 100)

    # ECU measures volume in [mL]
    @staticmethod
    def ecu_to_ml(vol: int) -> float:
        return float(vol)

    @staticmethod
    def ml_to_ecu(vol: float) -> int:
        return int(vol)

    # ECU measures pressure in [0.1mmH2O]
    @staticmethod
    def ecu_to_cmh2o(pres: int) -> float:
        return float(pres) * 0.01

    @staticmethod
    def cmh2o_to_ecu(pres: float) -> int:
        return int(pres * 100)
