class FilterModule:
    def filters(self):
        return {"human": self.human_readable}

    def human_readable(self, value):
        units = ("K", "M", "G")
        i = 0
        unit = ""
        value = float(value)
        while value >= 1000 and i < len(units):
            unit = units[i]
            value /= 1000
            i += 1
        if unit == "":
            return str(int(value))
        if value < 100:
            return f"{value:.1f}{unit}"
        return f"{value:.0f}{unit}"
