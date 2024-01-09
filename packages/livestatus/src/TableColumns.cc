// Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
// This file is part of Checkmk (https://checkmk.com). It is subject to the
// terms and conditions defined in the file COPYING, which is part of this
// source code package.

#include "livestatus/TableColumns.h"

#include <memory>
#include <utility>

#include "livestatus/Column.h"
#include "livestatus/Query.h"
#include "livestatus/Row.h"
#include "livestatus/StringColumn.h"

using row_type = Column;

using namespace std::string_literals;

namespace {
constexpr const char *typenames[8] = {"int",  "float", "string", "list",
                                      "time", "dict",  "blob",   "null"};
}

TableColumns::TableColumns() {
    const ColumnOffsets offsets{};
    addColumn(std::make_unique<StringColumn<row_type>>(
        "table", "The name of the table", offsets, [this](const row_type &row) {
            for (const auto &[name, table] : tables_) {
                if (table->any_column(
                        [&](const auto &c) { return c.get() == &row; })) {
                    return table->name();
                }
            }
            return ""s;  // never reached if no bug
        }));
    addColumn(std::make_unique<StringColumn<row_type>>(
        "name", "The name of the column within the table", offsets,
        [](const row_type &row) { return row.name(); }));
    addColumn(std::make_unique<StringColumn<row_type>>(
        "description", "A description of the column", offsets,
        [](const row_type &row) { return row.description(); }));
    addColumn(std::make_unique<StringColumn<row_type>>(
        "type", "The data type of the column (int, float, string, list)",
        offsets, [](const row_type &row) {
            return typenames[static_cast<int>(row.type())];
        }));
}

std::string TableColumns::name() const { return "columns"; }

std::string TableColumns::namePrefix() const { return "column_"; }

void TableColumns::addTable(const Table &table) {
    tables_[table.name()] = &table;
}

void TableColumns::answerQuery(Query &query, const User & /*user*/,
                               const ICore & /*core*/) {
    for (const auto &[name, table] : tables_) {
        table->any_column(
            [&](const auto &c) { return !query.processDataset(Row{c.get()}); });
    }
}
