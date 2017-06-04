'''Import app object'''
from __init__ import *
'''Import flask objects'''
from flask import render_template, request, url_for, redirect


def load_note_into_form(note_form, single_note):
    '''load note note_title, body, creation and modification date from database
    into the form object, so when rendering, this datas will be
    automatically loaded this could be also done from template
    but all logics only in the backend is more efficient'''
    note_form.note_title.data = single_note.get_title()
    note_form.note_body.data = single_note.get_body()
    note_form.note_creation_date.raw_data = single_note.get_creation_date()
    note_form.note_modification_date.raw_data = single_note.get_modification_date()


def get_all_sections(section_id):
    '''get all sections from database'''
    current_section = Section.query.get_or_404(section_id)
    parent_notebook = current_section.get_notebook_id()
    sections = Section.query.filter_by(notebook_id=parent_notebook).order_by(Section.title).all()
    return current_section, parent_notebook, sections


def get_all_notebooks(notebook_id):
    '''get all notebooks from database'''
    current_notebook = Notebook.query.get_or_404(notebook_id)
    notebooks = Notebook.query.all()
    return current_notebook, notebooks


def get_all_and_single_notes(section_id):
    '''get all notes of a section from database in a descending order'''
    all_notes = Note.query.filter_by(section_id=section_id).order_by(Note.creation_date.desc()).all()
    single_note = Note.query.filter_by(section_id=section_id).order_by(Note.modification_date.desc()).first()
    return all_notes, single_note


@app.route('/<int:note_id>', methods=['GET', 'POST'])
def default_view(note_id=None):
    '''default view when app starts;
    also loading a note executes this view'''
    '''if note_id is not given
    loads last modified note'''
    if note_id is None:
        single_note = Note.query.order_by(Note.modification_date.desc()).first()
    else:
        single_note = Note.query.get_or_404(note_id)
    '''get all notes of a section from database in a descending order'''
    parent_section = single_note.get_section_id()
    all_notes = Note.query.filter_by(section_id=parent_section).order_by(Note.creation_date.desc()).all()
    '''get all sections from database'''
    current_section, parent_notebook, sections = get_all_sections(parent_section)
    '''get all notebooks from database'''
    current_notebook, notebooks = get_all_notebooks(parent_notebook)
    '''note button'''
    note_form = NotesForm()
    if note_form.note_new_btn.data:
        return redirect(url_for('new_note_view', parent_section=parent_section))
    if note_form.note_save_btn.data:
        single_note.set_title(note_form.note_title.data)
        single_note.set_preview(note_form)
        single_note.set_body(note_form)
        single_note.set_creation_date(note_form)
        single_note.set_modification_date()
        db.session.commit()
    if note_form.note_delete_btn.data:
        db.session.delete(single_note)
        db.session.commit()
        return redirect(url_for('section_view', section_id=parent_section))
    '''load note in from'''
    load_note_into_form(note_form, single_note)
    '''section button'''
    section_form = SectionForm()
    if section_form.section_new_btn.data:
        if section_form.section_new_title.data != '':
            section = Section()
            section.set_title(section_form.section_new_title.data)
            section.set_notebook_id(parent_notebook)
            db.session.add(section)
            db.session.commit()
            new_section_id = section.get_id()
            return redirect(url_for('section_view', section_id=new_section_id))
    if section_form.section_save_btn.data:
        if section_form.section_current_title.data != '':
            current_section.set_title(section_form.section_current_title.data)
            db.session.commit()
    if section_form.section_delete_btn.data:
        for note in all_notes:
            db.session.delete(note)
        db.session.delete(current_section)
        db.session.commit()
        return redirect(url_for('notebook_view', notebook_id=parent_notebook))
    try:
        section_form.section_current_title.data = current_section.get_title()
    except:
        section_form.section_current_title.data = ''
    '''notebook button'''
    notebook_form = NotebookForm()
    if notebook_form.notebook_new_btn.data:
        if notebook_form.notebook_new_title.data != '':
            notebook = Notebook()
            notebook.set_title(notebook_form.notebook_new_title.data)
            db.session.add(notebook)
            db.session.commit()
            new_notebook_id = notebook.get_id()
            return redirect(url_for('notebook_view', notebook_id=new_notebook_id))
    if notebook_form.notebook_save_btn.data:
        if notebook_form.notebook_current_title.data != '':
            current_notebook.set_title(notebook_form.notebook_current_title.data)
            db.session.commit()
    notebook_form.notebook_current_title.data = current_notebook.get_title()
    '''rendering note from database'''
    return (render_template('base.html', note_form=note_form,
            notebooks=notebooks, sections=sections, all_notes=all_notes,
            single_note=single_note, current_notebook=current_notebook,
            current_section=current_section, notebook_form=notebook_form,
            section_form=section_form))


@app.route('/section/<int:section_id>', methods=['GET', 'POST'])
def section_view(section_id):
    '''this view is executed
    when a section is clicked'''
    '''get all sections from database'''
    current_section, parent_notebook, sections = get_all_sections(section_id)
    '''get all notebooks from database'''
    current_notebook, notebooks = get_all_notebooks(parent_notebook)
    '''get all notes and a single note of a section
    from database in a descending order'''
    all_notes, single_note = get_all_and_single_notes(section_id)
    '''note button'''
    note_form = NotesForm()
    if note_form.note_new_btn.data:
        return redirect(url_for('new_note_view', parent_section=section_id))
    if note_form.note_save_btn.data:
        single_note.set_title(note_form.note_title.data)
        single_note.set_preview(note_form)
        single_note.set_body(note_form)
        single_note.set_creation_date(note_form)
        single_note.set_modification_date()
        db.session.commit()
    if note_form.note_delete_btn.data:
        db.session.delete(single_note)
        db.session.commit()
        return redirect(url_for('section_view', section_id=section_id))
    if single_note is not None:
        load_note_into_form(note_form, single_note)
    else:
        '''when writing a new note, always set the creation date
        and modification date to current time
        btw creation date can be changed, but
        modification date can't be changed'''
        note_form.note_creation_date.raw_data = current_time()
        note_form.note_modification_date.raw_data = current_time()
    '''section button'''
    section_form = SectionForm()
    if section_form.section_new_btn.data:
        if section_form.section_new_title.data != '':
            section = Section()
            section.set_title(section_form.section_new_title.data)
            section.set_notebook_id(parent_notebook)
            db.session.add(section)
            db.session.commit()
            new_section_id = section.get_id()
            return redirect(url_for('section_view', section_id=new_section_id))
    if section_form.section_save_btn.data:
        if section_form.section_current_title.data != '':
            current_section.set_title(section_form.section_current_title.data)
            db.session.commit()
    if section_form.section_delete_btn.data:
        for note in all_notes:
            db.session.delete(note)
        db.session.delete(current_section)
        db.session.commit()
        return redirect(url_for('notebook_view', notebook_id=parent_notebook))
    try:
        section_form.section_current_title.data = current_section.get_title()
    except:
        section_form.section_current_title.data = ''
    '''notebook button'''
    notebook_form = NotebookForm()
    if notebook_form.notebook_new_btn.data:
        if notebook_form.notebook_new_title.data != '':
            notebook = Notebook()
            notebook.set_title(notebook_form.notebook_new_title.data)
            db.session.add(notebook)
            db.session.commit()
            new_notebook_id = notebook.get_id()
            return redirect(url_for('notebook_view', notebook_id=new_notebook_id))
    if notebook_form.notebook_save_btn.data:
        if notebook_form.notebook_current_title.data != '':
            current_notebook.set_title(notebook_form.notebook_current_title.data)
            db.session.commit()
    notebook_form.notebook_current_title.data = current_notebook.get_title()
    '''rendering note from database'''
    return (render_template('base.html', note_form=note_form,
            notebooks=notebooks, sections=sections, all_notes=all_notes,
            single_note=single_note, current_notebook=current_notebook,
            current_section=current_section, notebook_form=notebook_form,
            section_form=section_form))


@app.route('/', methods=['GET', 'POST'])
@app.route('/notebook/<int:notebook_id>', methods=['GET', 'POST'])
def notebook_view(notebook_id=None):
    '''this view is executed
    when a notebook is clicked'''
    if notebook_id is None:
        current_notebook = ''
        try:
            notebooks = Notebook.query.all()
        except:
            notebooks = []
    else:
        '''get all notebooks from database'''
        current_notebook, notebooks = get_all_notebooks(notebook_id)
    '''get all sections of a notebook'''
    sections = Section.query.filter_by(notebook_id=notebook_id).order_by(Section.title).all()
    if len(sections) == 0:
        all_notes = []
        single_note = None
        current_section = []
    else:
        '''get all notes and a single note of a section
        from database in a descending order'''
        section_id = Section.query.filter_by(notebook_id=notebook_id).order_by(Section.title).first().get_id()
        current_section = Section.query.get_or_404(section_id)
        all_notes, single_note = get_all_and_single_notes(section_id)
    '''note button'''
    note_form = NotesForm()
    if note_form.note_new_btn.data:
        return redirect(url_for('new_note_view', parent_section=parent_section))
    if note_form.note_save_btn.data:
        single_note.set_title(note_form.note_title.data)
        single_note.set_preview(note_form)
        single_note.set_body(note_form)
        single_note.set_creation_date(note_form)
        single_note.set_modification_date()
        db.session.commit()
    if note_form.note_delete_btn.data:
        db.session.delete(single_note)
        db.session.commit()
        return redirect(url_for('section_view', section_id=parent_section))
    if single_note is not None:
        load_note_into_form(note_form, single_note)
    else:
        '''when writing a new note, always set the creation date
        and modification date to current time
        btw creation date can be changed, but
        modification date can't be changed'''
        note_form.note_creation_date.raw_data = current_time()
        note_form.note_modification_date.raw_data = current_time()
    '''section button'''
    section_form = SectionForm()
    if section_form.section_new_btn.data:
        if section_form.section_new_title.data != '':
            section = Section()
            section.set_title(section_form.section_new_title.data)
            section.set_notebook_id(notebook_id)
            db.session.add(section)
            db.session.commit()
            new_section_id = section.get_id()
            return redirect(url_for('section_view', section_id=new_section_id))
    if section_form.section_save_btn.data:
        if section_form.section_current_title.data != '':
            current_section.set_title(section_form.section_current_title.data)
            db.session.commit()
    if section_form.section_delete_btn.data:
        for note in all_notes:
            db.session.delete(note)
        db.session.delete(current_section)
        db.session.commit()
        return redirect(url_for('notebook_view', notebook_id=notebook_id))
    try:
        section_form.section_current_title.data = current_section.get_title()
    except:
        section_form.section_current_title.data = ''
    '''notebook button'''
    notebook_form = NotebookForm()
    if notebook_form.notebook_new_btn.data:
        if notebook_form.notebook_new_title.data != '':
            notebook = Notebook()
            notebook.set_title(notebook_form.notebook_new_title.data)
            db.session.add(notebook)
            db.session.commit()
            new_notebook_id = notebook.get_id()
            return redirect(url_for('notebook_view', notebook_id=new_notebook_id))
    if notebook_form.notebook_save_btn.data:
        if notebook_form.notebook_current_title.data != '':
            current_notebook.set_title(notebook_form.notebook_current_title.data)
            db.session.commit()
    try:
        notebook_form.notebook_current_title.data = current_notebook.get_title()
    except:
        notebook_form.notebook_current_title.data = ''
    '''rendering note from database'''
    return (render_template('base.html', note_form=note_form,
            notebooks=notebooks, sections=sections, all_notes=all_notes,
            single_note=single_note, current_notebook=current_notebook,
            current_section=current_section, notebook_form=notebook_form,
            section_form=section_form))


@app.route('/new_note/<int:parent_section>', methods=['GET', 'POST'])
def new_note_view(parent_section):
    '''view when creating a new note'''
    '''get all notes of a section from database in a descending order'''
    all_notes = Note.query.filter_by(section_id=parent_section).order_by(Note.creation_date.desc()).all()
    '''get all sections from database'''
    current_section, parent_notebook, sections = get_all_sections(parent_section)
    '''get all notebooks from database'''
    current_notebook, notebooks = get_all_notebooks(parent_notebook)
    '''note button'''
    note_form = NotesForm()
    if note_form.note_new_btn.data:
        return redirect(url_for('new_note_view', parent_section=parent_section))
    if note_form.note_save_btn.data:
        single_note = Note()
        single_note.set_title(note_form.note_title.data)
        single_note.set_preview(note_form)
        single_note.set_body(note_form)
        single_note.set_creation_date(note_form)
        single_note.set_modification_date()
        single_note.set_section_id(parent_section)
        db.session.add(single_note)
        db.session.commit()
        new_note_id = single_note.get_id()
        return redirect(url_for('default_view', note_id=new_note_id))
    note_form.note_creation_date.raw_data = current_time()
    note_form.note_modification_date.raw_data = current_time()
    '''section button'''
    section_form = SectionForm()
    if section_form.section_new_btn.data:
        if section_form.section_new_title.data != '':
            section = Section()
            section.set_title(section_form.section_new_title.data)
            section.set_notebook_id(parent_notebook)
            db.session.add(section)
            db.session.commit()
            new_section_id = section.get_id()
            return redirect(url_for('section_view', section_id=new_section_id))
    if section_form.section_save_btn.data:
        if section_form.section_current_title.data != '':
            current_section.set_title(section_form.section_current_title.data)
            db.session.commit()
    try:
        section_form.section_current_title.data = current_section.get_title()
    except:
        section_form.section_current_title.data = ''
    '''notebook button'''
    notebook_form = NotebookForm()
    if notebook_form.notebook_new_btn.data:
        if notebook_form.notebook_new_title.data != '':
            notebook = Notebook()
            notebook.set_title(notebook_form.notebook_new_title.data)
            db.session.add(notebook)
            db.session.commit()
            new_notebook_id = notebook.get_id()
            return redirect(url_for('notebook_view', notebook_id=new_notebook_id))
    if notebook_form.notebook_save_btn.data:
        if notebook_form.notebook_current_title.data != '':
            current_notebook.set_title(notebook_form.notebook_current_title.data)
            db.session.commit()
    notebook_form.notebook_current_title.data = current_notebook.get_title()
    '''rendering note from database'''
    return (render_template('base.html', note_form=note_form,
            notebooks=notebooks, sections=sections, all_notes=all_notes,
            current_notebook=current_notebook,
            current_section=current_section, notebook_form=notebook_form,
            section_form=section_form))

