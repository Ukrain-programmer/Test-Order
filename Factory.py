from Gener_class import *
from Repository import *

class Factory:

    def call_builder_record(self):
        repository = Repository()
        build = Builder_record(repository)
        build.build()
        build.get_dto_to_reposetiry()








class Builder_record:

    def __init__(self, repository :Repository):
        self.repository = repository
        self.config = Config()
        self.id = ID(self.config)
        self.instrument = Instrument(self.config, self.id)
        self.px_init = None
        self.px_fill  = None
        self.status = Status(self.config)
        self.site = Side(self.config, self.id)
        self.volume_init = Volum_init(self.config, self.id)
        self.volum_fill = Volum_fill(self.config, self.volume_init, self.status, self.id)
        self.date = Date(self.config, self.id, self.status)
        self.note = Note(self.config, self.date, self.id)
        self.tag = Tag(self.config, self.date, self.id)

    def build(self):
        self.id = self.id.getData()
        self.instrument, self.px_init, self.px_fill = self.instrument.getData()
        self.status = self.status.getData()
        self.site = self.site.getData()
        self.volume_init = self.volume_init.getData()
        self.volum_fill = self.volum_fill.getData()
        self.date = self.date.getData()
        self.note = self.note.getData()
        self.tag = self.tag.getData()

    def get_dto_to_reposetiry(self):
        dto = DataMaping(self.id ,self.instrument ,self.px_init ,self.px_fill ,self.site ,self.volume_init, self.volum_fill, self.date ,self.status ,self.note ,self.tag)
        self.repository.set_to_dictionary(dto)
        self.repository.to_file_csv()


if __name__ == '__main__':
    factory = Factory()
    factory.call_builder_record()

