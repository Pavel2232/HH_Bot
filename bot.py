import re

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from aiogram.utils.markdown import hlink, hbold
from environs import Env
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text

from DataClass import DetailVacancyResponse
from main import HeadHunterPars

env = Env()
env.read_env('.env_ci')
logging.basicConfig(level=logging.INFO)
bot = Bot(token=env('TG_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
hh = HeadHunterPars(params={})
KEY = ''


class StateParamas(StatesGroup):
    text = State()
    area = State()
    end = State()


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder='Старт', one_time_keyboard=True)
    markup.add(types.KeyboardButton(text='начать'))
    await message.answer("Привет! \n Я бот который поможет найти работу!", reply_markup=markup)


@dp.message_handler(Text(equals='сброс поиска'))
async def reset(message: types.Message, state: FSMContext):
    await state.reset_state()
    await cmd_start(message)


@dp.message_handler(Text(equals='начать'))
async def text(message: types.Message):
    await message.answer("введите название вакансии")
    await StateParamas.text.set()


@dp.message_handler(Text(equals='сопроводительное письмо создать?'))
async def create_letter(message: types.Message):
    markup = markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder='назад')
    markup.add(types.KeyboardButton(text='👈назад'))
    markup.add(types.KeyboardButton(text='сброс поиска'))
    vacancy: DetailVacancyResponse = hh.dict_vacancy.get(KEY)
    my_letter = f'''Добрый день!
Прошу рассмотреть мое резюме на вакансию "{vacancy.name}".
Уверен, что могу быть вам полезен, так как:
- Знаю теорию и основы Python-программирования,
- Обладаю навыками работы с фреймворками Flask и Django,
- Использовал Git,Yandex cloud
- Знаю SQL: умение оптимизировать и составлять сложные SQL-запросы, PostgreSQL,
- Обладаю базовыми знаниями ORM и миграций,
- Есть навыки работы с SQlite3 и PostgreSQL,
- Знаю HTML и CSS на базовом уровне,
- Знаю Docker и Docker-сompose,
- Обладаю базовыми знаниями CI/CD,
- Тестировал веб-приложения,
- Понимаю JWT, OAuth2.0,
- Умею работать в команде и в индивидуальном формате.
Ваша компания меня заинтересовала у вас очень интересный проект и я безумно хочу в нем поучаствовать. 
Уверен, что справлюсь с поставленными задачами на 100%, так как уже решал подобные кейсы в процессе обучения и практики. 
Буду рад стать частью профессиональной команды. Готов подробно рассказать о своём опыте и знаниях.
Мазикин Павел
тел. 8-977-729-48-38
GitHub: https://github.com/Pavel2232
E-mail pavelmazikinvladimirovich@gmail.com
Буду очень благодарен за любую обратную связь.'''
    await message.answer(my_letter, reply_markup=markup)


@dp.message_handler(state=StateParamas.text)
async def tt(message: types.Message, state: FSMContext):
    await state.update_data(chosen_text=message.text.lower())
    await StateParamas.area.set()
    chouse = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder='Выбирете')
    chouse.add(types.KeyboardButton(text='Москва'))
    chouse.add(types.KeyboardButton(text='Россия'))
    await message.answer('выберете', reply_markup=chouse)


@dp.message_handler(Text(equals='👉далее'))
async def next_page(message: types.Message):
    hh.netx_page(1)
    await get(message)


@dp.message_handler(state=StateParamas.area)
async def tt(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder='Выбирете')
    markup.add(types.KeyboardButton(text='получить вакансии'))
    markup.add(types.KeyboardButton(text='сброс поиска'))
    if message.text.lower() == 'москва':
        await state.update_data(area=1)
    elif message.text.lower() == 'россия':
        await state.update_data(area=113)
    await StateParamas.end.set()
    await state.reset_state(with_data=False)
    text = await state.get_data()
    if text.get('area') != None:
        hh.set_params(text=text.get('chosen_text'), area=text.get('area'), page=0, per_page=5)
        await message.answer('Готовы к поиску', reply_markup=markup)
    else:
        await StateParamas.area.set()
        await message.answer('введите Москва или Россия')


@dp.message_handler(Text(equals='получить вакансии'))
async def get(message: types.Message):
    markup = markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder='следующая')
    markup.add(types.KeyboardButton(text='👉далее'))
    markup.add(types.KeyboardButton(text='сброс поиска'))
    itog = hh.get_detail_vacancy()
    for vacancy in itog:
        card = f'{hlink(vacancy.name, vacancy.alternate_url)}\n' \
               f'{hbold("Описание: ")}{vacancy.description[:50]}❤️‍🔥'
        await message.answer(card, reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def test_text(message: types.Message):
    try:
        key = message.reply_to_message.text.split('"')[1]
        global KEY
        KEY = key
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder='Выбирете',
                                           one_time_keyboard=True)
        markup.add(types.KeyboardButton(text='сопроводительное письмо создать?'))
        markup.add(types.KeyboardButton(text='сброс поиска'))
        markup.add(types.KeyboardButton(text='👉далее'))
        tt = hh.dict_vacancy.get(key)
        card = f'{hlink(tt.name, key)}\n' \
               f'{hbold("Описание: ")}{re.sub("<(.*?)>", " ", tt.description)}❤️‍🔥'
        await message.answer(card, reply_markup=markup)
    except AttributeError:
        await message.answer("Просто текст бот не поддерживает")


if __name__ == "__main__":
    executor.start_polling(dp)
