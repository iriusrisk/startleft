class ProjectTrustZone:
    def __init__(self, name, ref):
        self.name = name
        self.ref = ref

    def __eq__(self, other):
        if isinstance(other, ProjectTrustZone):
            return self.ref == other.ref
        else:
            return False

    def __hash__(self):
        return hash(self.ref)

    def __repr__(self):
        return "ProjectTrustZone(%s, %s)" % (self.name, self.ref)
