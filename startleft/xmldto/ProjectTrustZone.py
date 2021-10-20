class ProjectTrustZone:
    def __init__(self, name, ref, uuid, desc, trust_rating):
        self.name = name
        self.ref = ref
        self.uuid = uuid
        self.desc = desc
        self.trust_rating = trust_rating

    def __eq__(self, other):
        if isinstance(other, ProjectTrustZone):
            return self.ref == other.ref and self.uuid == other.uuid
        else:
            return False

    def __hash__(self):
        return hash(self.ref + self.uuid)

    def __repr__(self):
        return "ProjectTrustZone(%s, %s, %s)" % (self.name, self.ref, self.uuid)
